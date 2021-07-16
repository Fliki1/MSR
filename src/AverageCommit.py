import csv
import time
import logging

from src import ProgressionBar
from pydriller import Repository
from pydriller import Git
from tabulate import tabulate

import numpy as np

logger = logging.getLogger(__name__)  # nome del modulo corrente (AverageCommit.py)


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
    file_handler = logging.FileHandler('./log/AverageCommit.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def print_tabulate(repo_list, headers, average_matrix):
    """ Tabulate and print """
    # Rendo vettore colonna i nomi dei repo
    repo_name_col = np.array(repo_list)
    repo_name_col.shape = (len(repo_list), 1)
    # Unisco i nomi dei repo alla matrice di conteggio commit per giorni della settimana
    average_matrix_new = np.hstack((repo_name_col, average_matrix))
    print(tabulate(average_matrix_new, headers=headers, tablefmt="simple"))


def bar_view(repo, repo_index, total_commits, average_matrix):
    """ Average commit: bar console, non buono per benchmark visto il 0.1s di delay """
    for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                             prefix='Progress:', suffix='Complete', length=50):
        logger.info(f'Hash {commit.hash}: Average {"""commit.committer_date.hour"""}')
        average_matrix[repo_index, """commit.committer_date.hour"""] += 1
        time.sleep(0.1)
    return average_matrix


def log_view(repo, repo_index, total_commits, average_matrix):
    """ Average commit: log console """
    commit_count = 1
    for commit in Repository(path_to_repo=repo).traverse_commits():
        logger.info(f'{commit_count}/{total_commits}: Hash {commit.hash}: Average {"""commit.committer_date.hour"""}')
        commit_count += 1
        #average_matrix[repo_index, """commit.committer_date.hour"""] += 1
    return average_matrix


def repo_list(urls):
    """ Lista nomi dei progetti dei git urls """
    rep_list = []
    for proj in urls:
        repo = Repository(path_to_repo=proj).traverse_commits()
        commit = next(repo)
        rep_list.append(commit.project_name)
    return rep_list


def csv_generation(repo_list, headers, average_commit):
    """ Generazione dei file CSV """
    csv_headers = ["Commit_hash", "Activity_Score"]
    row_project = 0
    for repo_name in repo_list:
        with open("./data-results/average_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            for i, entry in enumerate(average_commit[row_project]):
                # riga del csv
                writer.writerow({csv_headers[0]: headers[i + 1],    # Commit_hash
                                 csv_headers[1]: entry})            # Activity_Score
        # next project
        row_project += 1
        logger.info(f'Average Commit: {repo_name} ✔')


def average_commit(urls, average_file_type, verbose):
    """ Invoca metodo di analisi: Average Commits """
    # Setting log
    log(verbose)

    # Tag per i file csv: no header in quanto non ho una misura precisa
    # headers = ["Nome repo.", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10","11", "12", "13", "14", "15", "16", "17", "18", "19", "20","21", "22", "23"]

    # Matrice: riga il progetto, colonna count del giorno corrispettivo
    average_matrix = np.zeros(((len(urls)), 24), dtype=int)

    # Indice del repo corrente sotto analisi
    repo_index = 0

    rep_list = repo_list(urls)

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(average_commit) Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits
        if verbose:  # log file + console
            average_matrix = log_view(url, repo_index, git.total_commits(), average_matrix)
        else:  # log file
            average_matrix = bar_view(url, repo_index, git.total_commits(), average_matrix)
        repo_index += 1

    # Stampo a video il risultato
    print_tabulate(rep_list, headers, average_matrix)

    # CSV file
    csv_generation(rep_list, headers, average_matrix)