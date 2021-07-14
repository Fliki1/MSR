import csv
import time
import logging

from src import ProgressionBar
from pydriller import Repository
from pydriller import Git
from tabulate import tabulate

import numpy as np

logger = logging.getLogger(__name__)  # nome del modulo corrente (main.py)


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
    file_handler = logging.FileHandler('./log/HourCommit.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def print_tabulate(repo_list, headers, hour_matrix):
    """ Tabulate and print """
    # Rendo vettore colonna i nomi dei repo
    repo_name_col = np.array(repo_list)
    repo_name_col.shape = (len(repo_list), 1)
    # Unisco i nomi dei repo alla matrice di conteggio commit per giorni della settimana
    hour_matrix_new = np.hstack((repo_name_col, hour_matrix))
    print(tabulate(hour_matrix_new, headers=headers, tablefmt="simple"))


def bar_view(repo, repo_index, total_commits, hour_matrix):
    """ Hour commit: bar console, non buono per benchmark visto il 0.1s di delay """
    for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                             prefix='Progress:', suffix='Complete', length=50):
        logger.info(f'Hash {commit.hash}: Hour {commit.committer_date.hour}')
        hour_matrix[repo_index, commit.committer_date.hour] += 1
        time.sleep(0.1)
    return hour_matrix


def log_view(repo, repo_index, total_commits, hour_matrix):
    """ Hour commit: log console """
    commit_count = 1
    for commit in Repository(path_to_repo=repo).traverse_commits():
        logger.info(f'{commit_count}/{total_commits}: Hash {commit.hash}: Hour {commit.committer_date.hour}')
        commit_count += 1
        hour_matrix[repo_index, commit.committer_date.hour] += 1
    return hour_matrix


def repo_list(urls):
    """ Lista nomi dei progetti dei git urls """
    rep_list = []
    for proj in urls:
        repo = Repository(path_to_repo=proj).traverse_commits()
        commit = next(repo)
        rep_list.append(commit.project_name)
    return rep_list


def csv_generation(repo_list, headers, hour_commit):
    """ Generazione dei file CSV """
    row_project = 0
    for repo_name in repo_list:
        with open("./data-results/hour_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            # riga del csv
            writer.writerow({headers[0]: repo_name,
                             headers[1]: hour_commit[row_project][0],
                             headers[2]: hour_commit[row_project][1],
                             headers[3]: hour_commit[row_project][2],
                             headers[4]: hour_commit[row_project][3],
                             headers[5]: hour_commit[row_project][4],
                             headers[6]: hour_commit[row_project][5],
                             headers[7]: hour_commit[row_project][6],
                             headers[8]: hour_commit[row_project][7],
                             headers[9]: hour_commit[row_project][8],
                             headers[10]: hour_commit[row_project][9],
                             headers[11]: hour_commit[row_project][10],
                             headers[12]: hour_commit[row_project][11],
                             headers[13]: hour_commit[row_project][12],
                             headers[14]: hour_commit[row_project][13],
                             headers[15]: hour_commit[row_project][14],
                             headers[16]: hour_commit[row_project][15],
                             headers[17]: hour_commit[row_project][16],
                             headers[18]: hour_commit[row_project][17],
                             headers[19]: hour_commit[row_project][18],
                             headers[20]: hour_commit[row_project][19],
                             headers[21]: hour_commit[row_project][20],
                             headers[22]: hour_commit[row_project][21],
                             headers[23]: hour_commit[row_project][22],
                             headers[24]: hour_commit[row_project][23]})
        # next project
        row_project += 1
        logger.info(f'Hour Commit: {repo_name} ✔')


def hour_commit(urls, verbose):
    """ Invoca metodo di analisi: Hour Commits """
    # Setting log
    log(verbose)

    # Tag per i file csv
    headers = ["Nome repo.", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
               "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
               "21", "22", "23"]

    # Matrice: riga il progetto, colonna count del giorno corrispettivo
    hour_matrix = np.zeros(((len(urls)), 24), dtype=int)

    # Indice del repo corrente sotto analisi
    repo_index = 0

    rep_list = repo_list(urls)

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(hour_commit) Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits
        if verbose:  # log file + console
            hour_matrix = log_view(url, repo_index, git.total_commits(), hour_matrix)
        else:  # log file
            hour_matrix = bar_view(url, repo_index, git.total_commits(), hour_matrix)
        repo_index += 1

    # Stampo a video il risultato
    print_tabulate(rep_list, headers, hour_matrix)

    # CSV file
    csv_generation(rep_list, headers, hour_matrix)
