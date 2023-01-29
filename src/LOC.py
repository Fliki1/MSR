import csv
import time
import logging

from src import ProgressionBar
from pydriller import Repository
from pydriller import Git

import numpy as np

logger = logging.getLogger(__name__)  # nome del modulo corrente (LOC.py)


def log(verbos):
    """ Setto i parametri per gestire il file di log (unici per modulo magari) """
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    if verbos:
        # StreamHandler: console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    # FileHandler: outputfile
    file_handler = logging.FileHandler('./log/LOC.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def bar_view(repo, repo_name, total_commits, csv_headers):
    """ LOC: bar console, non buono per benchmark visto il 0.1s di delay """
    with open("./data-results/loc_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        total_line = 0
        for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                                 prefix='Progress:', suffix='Complete', length=50):

            logger.info(f'Hash: {commit.hash}, '
                        f'Add: {commit.insertions}, '
                        f'Del: {commit.deletions}, '
                        f'Time: {commit.committer_date}')

            total_line += commit.insertions - commit.deletions
            # print(commit.committer_date.strftime("%d/%m/%Y"))
            writer.writerow({csv_headers[0]: commit.hash,  # Hash
                             csv_headers[1]: total_line,  # loc
                             csv_headers[2]: commit.committer_date.strftime("%d/%m/%Y")})  # Time
            time.sleep(0.1)
    logger.info(f'LOC Commit: {repo_name} ✔')


def log_view(repo, repo_name, csv_headers):
    """ LOC: bar console, non buono per benchmark visto il 0.1s di delay """
    with open("./data-results/loc_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        total_line = 0
        for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                                 prefix='Progress:', suffix='Complete', length=50):

            logger.info(f'Hash: {commit.hash}, '
                        f'Add: {commit.insertions}, '
                        f'Del: {commit.deletions}, '
                        f'Time: {commit.committer_date}')

            total_line += commit.insertions - commit.deletions

            writer.writerow({csv_headers[0]: commit.hash,  # Hash
                             csv_headers[1]: total_line,  # loc
                             csv_headers[2]: commit.committer_date})  # Time
    logger.info(f'LOC Commit: {repo_name} ✔')



def loc_commit(urls, verbose):
    """ Invoca metodo di analisi: LOC Commits """
    # Setting log
    log(verbose)

    # csv header
    csv_headers = ["Commit_hash", "LOC", "Time"]

    # Indice del repo corrente sotto analisi
    repo_index = 0

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(loc_commit) Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits
        if verbose:  # log file + console
            log_view(url, commit.project_name, csv_headers)
        else:  # log file
            bar_view(url, commit.project_name, git.total_commits(), csv_headers)
        repo_index += 1

