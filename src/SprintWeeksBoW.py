import csv
import time
import logging
from src import ProgressionBar
from pydriller import Repository
from pydriller import Git

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

    with open("./data-results/bow_sprint_week_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        prec_commit = None

        for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                                 prefix='Progress:', suffix='Complete', length=50):

            logger.info(f'Hash: {commit.hash}, '
                        f'Week: {commit.committer_date.isocalendar()[1]}, '
                        f'Time: {commit.committer_date}, '
                        f'Messaggio: {commit.msg}')

            if prec_commit == None:  # Forse senza if e prec_commit = commit standard a ogni ciclo
                prec_commit = commit
                msg_commit = commit.msg  # add msg commit
                continue

            # conteggio dei commit: della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                    prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                msg_commit = msg_commit + " " + commit.msg
            else:  # cambio di settimana salvo gli esiti
                writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Day
                                 csv_headers[1]: prec_commit.committer_date.isocalendar()[1],  # Week
                                 csv_headers[2]: msg_commit})  # Msg_data
                msg_commit = commit.msg  # reset
            prec_commit = commit
            time.sleep(0.1)
        # last week
        writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Day
                         csv_headers[1]: prec_commit.committer_date.isocalendar()[1],  # Week
                         csv_headers[2]: msg_commit})  # Msg_data
    logger.info(f'BoW Sprint Week: {repo_name} ✔')


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
                msg_commit = commit.msg    # add msg commit
                continue

            # conteggio dei commit: della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                    prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                msg_commit = msg_commit +" "+ commit.msg
            else:  # cambio di settimana salvo gli esiti
                writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Day
                                 csv_headers[1]: prec_commit.committer_date.isocalendar()[1],  # Week
                                 csv_headers[2]: msg_commit})  # Msg_data
                msg_commit = commit.msg  #reset
            prec_commit = commit
        # last week
        writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Day
                         csv_headers[1]: prec_commit.committer_date.isocalendar()[1],  # Week
                         csv_headers[2]: msg_commit})  # Msg_data
    logger.info(f'BoW Sprint Week: {repo_name} ✔')

def sprint_commit_bow(urls, verbose):
    """ Invoca metodo di analisi: Sprint Week Commits BoW"""
    # Setting log
    log(verbose)

    # csv header
    csv_headers = ["Day", "Week", "Msg_data"]

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

    # ML?
