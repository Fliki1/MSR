import csv
import time
import logging
import os
from src import ProgressionBar
from pydriller import Repository
from pydriller import Git
from git import Repo

logger = logging.getLogger(__name__)  # nome del modulo corrente (SprintWeeksBoW.py)


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
    file_handler = logging.FileHandler('./log/SprintBowLog.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def bar_view(repo, repo_name, total_commits, csv_headers):
    """ Sprint Weeks: bar console, non buono per benchmark visto il 0.1s di delay """
    author = []
    with open("./data-results/bow_sprint_week_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        week_commit = 0
        prec_commit = None
        for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                                 prefix='Progress:', suffix='Complete', length=50):

            if commit.author.email not in author:
                author.append(commit.author.email)

            logger.info(f'Hash: {commit.hash}, '
                        f'Week: {commit.committer_date.isocalendar()[1]}, '
                        f'Time: {commit.committer_date}, '
                        f'Author: {commit.author.email}')

            if prec_commit == None:
                prec_commit = commit
                week_commit = week_commit + 1
                continue

            # conteggio commit della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                week_commit = week_commit + 1
            else:   # cambio di settimana salvo gli esiti
                writer.writerow({csv_headers[0]: commit.committer_date,  # Time
                                 csv_headers[1]: week_commit,  # Commit della settimana
                                 csv_headers[2]: commit.committer_date.isocalendar()[1], # Week
                                 csv_headers[3]: len(author)})  # Authors
                week_commit = 1     # reset
                author = []
            prec_commit = commit
            time.sleep(0.1)
    logger.info(f'Sprint Week: {repo_name} ✔')


def log_view(repo, repo_name, csv_headers):
    """ Sprint Weeks: log console """
    with open("./data-results/bow_sprint_week_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        msg_commit = ""
        prec_commit = None
        for commit in Repository(path_to_repo=repo).traverse_commits():

            logger.info(f'Hash: {commit.hash}, '
                        f'Week: {commit.committer_date.isocalendar()[1]}, '
                        f'Time: {commit.committer_date}, '
                        f'Messaggio: {commit.msg}')

            if prec_commit == None:  # Forse senza if e prec_commit = commit standard a ogni ciclo
                prec_commit = commit
                msg_commit = msg_commit +" "+ commit.msg    # add msg commit #TODO: vedere se settare direttamente commit.msg
                continue

            # conteggio dei commit: della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                    prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                msg_commit = msg_commit +" "+ commit.msg
            else:  # cambio di settimana salvo gli esiti
                writer.writerow({csv_headers[0]: commit.committer_date,  # Day
                                 csv_headers[1]: commit.committer_date.isocalendar()[1],  # Week
                                 csv_headers[2]: msg_commit})  # Msg_data
                msg_commit = ""  #reset
            prec_commit = commit
    logger.info(f'BoW Sprint Week: {repo_name} ✔')


def sprint_commit_bow(urls, verbose):
    """ Invoca metodo di analisi: Sprint Week Commits BoW"""
    # Setting log
    log(verbose)

    # csv header
    csv_headers = ["Day", "Week", "Msg_data"]

    # Indice del repo corrente sotto analisi
    repo_index = 0

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(sprint_week_bow) Project: {commit.project_name}')

        # Repo info
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits

        # Sprint in all repo
        if verbose:  # log file + console
            log_view(url, commit.project_name, csv_headers)
        else:  # log file
            bar_view(url, commit.project_name, git.total_commits(), csv_headers)

        """# Sprint in all Branch
        r = Repo(commit.project_path)
        remote_refs = r.remote().refs

        for refs in remote_refs:
            print(f'(sprint_week_commit) Project: {commit.project_name} Branch: {refs.name}')
            branch_view(url, refs.name, commit.project_name, git.total_commits(), csv_headers)
        repo_index += 1"""
