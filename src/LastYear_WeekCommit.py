import csv
import time
import logging
import datetime

from src import ProgressionBar
from pydriller import Repository
from pydriller import Git
from tabulate import tabulate
import numpy as np

logger = logging.getLogger(__name__)  # nome del modulo corrente (LastYear_WeekCommit.py)


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
    file_handler = logging.FileHandler('./log/LastYear_WeekCommit.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def bar_view(repo, repo_index, total_commits, year_matrix):
    """ Last year week commit: bar console, non buono per benchmark visto il 0.1s di delay """
    for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                             prefix='Progress:', suffix='Complete', length=50):
        logger.info(f'Hash {commit.hash}: WeekYear {commit.committer_date.isocalendar()[1]}')
        year_matrix[repo_index, commit.committer_date.isocalendar()[1]] += 1
        time.sleep(0.1)
    return year_matrix


def log_view(repo, repo_index, total_commits, year_matrix):
    """ Last year week commit: log console """
    commit_count = 1
    for commit in Repository(path_to_repo=repo).traverse_commits():
        logger.info(f'{commit_count}/{total_commits}: Hash {commit.hash}: Hour {commit.committer_date.isocalendar()[1]}')
        commit_count += 1
        year_matrix[repo_index, commit.committer_date.isocalendar()[1]] += 1
    return year_matrix


def repo_list(urls):
    """ Lista nomi dei progetti dei git urls """
    rep_list = []
    for proj in urls:
        repo = Repository(path_to_repo=proj).traverse_commits()
        commit = next(repo)
        rep_list.append(commit.project_name)
    return rep_list


def csv_generation(repo_list, headers, year_commit):
    """ Generazione dei file CSV """
    csv_headers = ["Last_Year_Week", "Count_week"]
    row_project = 0
    for repo_name in repo_list:
        with open("./data-results/lastyearweek_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            for i, entry in enumerate(year_commit[row_project]):
                # riga del csv
                writer.writerow({csv_headers[0]: headers[i + 1],  # Hour_of_day
                                 csv_headers[1]: entry})  # Count_hour
        # next project
        row_project += 1
        logger.info(f'WeekYear Commit: {repo_name} ✔')


def last_year_week_commit(urls, verbose):
    """ Invoca metodo di analisi: Last year week Commit """
    # Setting log
    log(verbose)

    # Tag per i file csv
    headers = ["Nome repo.", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
               "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
               "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
               "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
               "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
               "51", "52"]


    # Matrice: riga il progetto, colonna count della settimana
    lastyear_matrix = np.zeros(((len(urls)), 53), dtype=int)

    # Indice del repo corrente sotto analisi
    repo_index = 0

    rep_list = repo_list(urls)

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(lastyear_commit) Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits
        if verbose:  # log file + console
            hour_matrix = log_view(url, repo_index, git.total_commits(), lastyear_matrix)
        else:  # log file
            hour_matrix = bar_view(url, repo_index, git.total_commits(), lastyear_matrix)
        repo_index += 1


    # CSV file
    csv_generation(rep_list, headers, lastyear_matrix)