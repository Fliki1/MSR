import csv
import time
import logging

from src import ProgressionBar
from pydriller import Repository
from pydriller import Git

import numpy as np

logger = logging.getLogger(__name__)  # nome del modulo corrente (LineCodeCommit.py)


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
    file_handler = logging.FileHandler('./log/LineCommit.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def bar_view(repo, repo_name, total_commits, csv_headers):
    """ Line commit: bar console, non buono per benchmark visto il 0.1s di delay """
    with open("./data-results/line_commit_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        total_line = 0
        prec_commit = None
        for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                                 prefix='Progress:', suffix='Complete', length=50):

            logger.info(f'Hash: {commit.hash}, '
                        f'Add: {commit.insertions}, '
                        f'Del: {commit.deletions}, '
                        f'Time: {commit.committer_date}')

            if prec_commit == None: # Forse senza if e prec_commit = commit standard a ogni ciclo
                prec_commit = commit
                total_line = total_line + prec_commit.insertions - prec_commit.deletions
                continue

            # conteggio delle line commit: della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                total_line = total_line + commit.insertions - commit.deletions
            else:   # cambio di settimana salvo gli esiti
                writer.writerow({csv_headers[0]: commit.committer_date,  # Time
                                 csv_headers[1]: total_line,  # Line
                                 csv_headers[2]: commit.committer_date.isocalendar()[1]})  # Week
            prec_commit = commit
            time.sleep(0.1)
    logger.info(f'Line Commit: {repo_name} ✔')


def log_view(repo, repo_name, total_commits, csv_headers):
    """ Line commit: log console """
    with open("./data-results/line_commit_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        total_line = 0
        for commit in Repository(path_to_repo=repo).traverse_commits():
            logger.info(f'Hash: {commit.hash}, '
                        f'Add: {commit.insertions}, '
                        f'Del: {commit.deletions}, '
                        f'Time: {commit.committer_date}')
            total_line = total_line + commit.insertions - commit.deletions
            writer.writerow({csv_headers[0]: commit.hash,  # Commit_hash
                             csv_headers[1]: total_line,  # Line
                             csv_headers[2]: commit.committer_date})  # Time
    logger.info(f'Line Commit: {repo_name} ✔')


def linecode_commit(urls, verbose):
    """ Invoca metodo di analisi: Line code Commits """
    # Setting log
    log(verbose)

    # csv header
    csv_headers = ["Commit_hash", "Line", "Time"]

    # Indice del repo corrente sotto analisi
    repo_index = 0

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(linecode_commit) Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits
        if verbose:  # log file + console
            log_view(url, commit.project_name, git.total_commits(), csv_headers)
        else:  # log file
            bar_view(url, commit.project_name, git.total_commits(), csv_headers)
        repo_index += 1

