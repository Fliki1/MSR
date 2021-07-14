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
    file_handler = logging.FileHandler('./log/WeekCommit.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def print_tabulate(repo_list, headers, week_matrix):
    """ Tabulate and print """
    # Rendo vettore colonna i nomi dei repo
    repo_name_col = np.array(repo_list)
    repo_name_col.shape = (len(repo_list), 1)
    # Unisco i nomi dei repo alla matrice di conteggio commit per giorni della settimana
    week_matrix_new = np.hstack((repo_name_col, week_matrix))
    print(tabulate(week_matrix_new, headers=headers, tablefmt="grid"))


def bar_view(repo, repo_index, total_commits, week_matrix):
    """ Weekly commit: bar console, non buono per benchmark visto il 0.1s di delay """
    for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                             prefix='Progress:', suffix='Complete', length=50):
        logger.info(f'Hash {commit.hash}: WeekDay {commit.committer_date.weekday()}')
        week_matrix[repo_index, commit.committer_date.weekday()] += 1
        time.sleep(0.1)
    return week_matrix


def log_view(repo, repo_index, total_commits, week_matrix):
    """ Weekly commit: log console """
    commit_count = 1
    for commit in Repository(path_to_repo=repo).traverse_commits():
        logger.info(f'{commit_count}/{total_commits}: Hash {commit.hash}: WeekDay {commit.committer_date.weekday()}')
        commit_count += 1
        week_matrix[repo_index, commit.committer_date.weekday()] += 1
    return week_matrix


def repo_list(urls):
    """ Lista nomi dei progetti dei git urls """
    rep_list = []
    for proj in urls:
        repo = Repository(path_to_repo=proj).traverse_commits()
        commit = next(repo)
        rep_list.append(commit.project_name)
    return rep_list


def csv_generation(repo_list, headers, week_commit):
    """ Generazione dei file CSV """
    row_project = 0
    for repo_name in repo_list:
        with open("./data-results/week_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            # riga del csv
            writer.writerow({headers[0]: repo_name,
                             headers[1]: week_commit[row_project][0],
                             headers[2]: week_commit[row_project][1],
                             headers[3]: week_commit[row_project][2],
                             headers[4]: week_commit[row_project][3],
                             headers[5]: week_commit[row_project][4],
                             headers[6]: week_commit[row_project][5],
                             headers[7]: week_commit[row_project][6]})
        # next project
        row_project += 1
        logger.info(f'Week Commit: {repo_name} ✔')


def week_commit(urls, verbose):
    """ Invoca metodo di analisi: Week Commits """
    # Setting log
    log(verbose)

    # Tag per i file csv
    headers = ["Nome repo.", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

    # Matrice: riga il progetto, colonna count del giorno corrispettivo
    week_matrix = np.zeros(((len(urls)), 7), dtype=int)

    # Indice del repo corrente sotto analisi
    repo_index = 0

    rep_list = repo_list(urls)

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(week_commit) Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits
        if verbose:  # log file + console
            week_matrix = log_view(url, repo_index, git.total_commits(), week_matrix)
        else:  # log file
            week_matrix = bar_view(url, repo_index, git.total_commits(), week_matrix)
        repo_index += 1

    # Stampo a video il risultato
    print_tabulate(rep_list, headers, week_matrix)

    # CSV file
    csv_generation(rep_list, headers, week_matrix)
