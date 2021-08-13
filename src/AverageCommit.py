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


def bar_view(repo, repo_name, total_commits, average_file_type, csv_headers):
    """ Average commit: bar console, non buono per benchmark visto il 0.1s di delay
        e anche il conteggio del calcolo: sum(1 for x in generator) oppure len(list(generator))"""
    # average_file_type
    if average_file_type is not None:
        with open("./data-results/average_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo,
                                                                only_modifications_with_file_types=[average_file_type]).traverse_commits(),
                                                     sum(1 for x in Repository(path_to_repo=repo,
                                                                only_modifications_with_file_types=[average_file_type]).traverse_commits()),
                                                     prefix='Progress:', suffix='Complete', length=50):
                logger.info(f'Hash: {commit.hash}, '
                            f'Average type: {average_file_type}, '
                            f'Added+Deleted: {commit.lines}, '
                            f'Time: {commit.committer_date}')
                writer.writerow({csv_headers[0]: commit.hash,  # Commit_hash
                                 csv_headers[1]: commit.lines,  # Commit_ADD_DEL
                                 csv_headers[2]: commit.committer_date})  # Time
                time.sleep(0.1)
        logger.info(f'Average Commit: {repo_name} ✔')
    else:   # no average_file_type
        commit_count = 1
        with open("./data-results/average_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(),
                                                     total_commits, prefix='Progress:', suffix='Complete', length=50):
                logger.info(
                    f'{commit_count}/{total_commits}: Hash: {commit.hash}, '
                    f'Average type: {average_file_type}, '
                    f'Added+Deleted: {commit.lines}, '
                    f'Time: {commit.committer_date}')
                writer.writerow({csv_headers[0]: commit.hash,  # Commit_hash
                                 csv_headers[1]: commit.lines,  # Commit_ADD_DEL
                                 csv_headers[2]: commit.committer_date})  # Time
                time.sleep(0.1)
            commit_count += 1
        logger.info(f'Average Commit: {repo_name} ✔')


def log_view(repo, repo_name, total_commits, average_file_type, csv_headers):
    """ Average commit: log console """
    if average_file_type is not None:
        with open("./data-results/average_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            for commit in Repository(path_to_repo=repo,
                                     only_modifications_with_file_types=[average_file_type]).traverse_commits():
                logger.info(f'Hash: {commit.hash}, '
                            f'Average type: {average_file_type}, '
                            f'Added+Deleted: {commit.lines}, '
                            f'Time: {commit.committer_date}')
                writer.writerow({csv_headers[0]: commit.hash,  # Commit_hash
                                 csv_headers[1]: commit.lines,  # Commit_ADD_DEL
                                 csv_headers[2]: commit.committer_date})  # Time
        logger.info(f'Average Commit: {repo_name} ✔')
    else:   # su tutto
        commit_count = 1
        with open("./data-results/average_commit_" + repo_name + ".csv", 'w') as f:
            # Header del csv
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            for commit in Repository(path_to_repo=repo).traverse_commits():
                logger.info(
                    f'{commit_count}/{total_commits}: Hash: {commit.hash}, '
                    f'Average type: {average_file_type}, '
                    f'Added+Deleted: {commit.lines}, '
                    f'Time: {commit.committer_date}')
                writer.writerow({csv_headers[0]: commit.hash,  # Commit_hash
                                 csv_headers[1]: commit.lines,  # Commit_ADD_DEL
                                 csv_headers[2]: commit.committer_date})  # Time
        logger.info(f'Average Commit: {repo_name} ✔')


def csv_sort(project_name):
    reader = csv.DictReader(open("./data-results/average_commit_" + project_name + ".csv", 'r'))
    result = sorted(reader, key=lambda d: int(d['ADD+DEL']))

    writer = csv.DictWriter(open("./data-results/average_commit_" + project_name + ".csv", 'w'), reader.fieldnames)
    writer.writeheader()
    writer.writerows(result)


def csv_avg(project_name, csv_headers):
    # open the file in universal line ending mode
    with open("./data-results/average_commit_" + project_name + ".csv", 'rU') as infile:
        # read the file as a dictionary for each row ({header : value})
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]

    # extract the variables
    hash_list = data['Commit_hash']
    time = data['Time']
    str_act_score = data['ADD+DEL']                 # calcolo della media: somma della lista/ len(int_list) arrotondato?
    int_act_score = list(map(int, str_act_score))   # str list in int list

    percentuale = round(len(int_act_score)*0.1)     # 10%
    #print('percentuale 10% ', percentuale)
    # prima bisogna levare gli estremi 10%, dalla risultante calcolarne la media
    avg = round(sum(int_act_score[percentuale:-percentuale])/len(int_act_score[percentuale:-percentuale]))    # average
    #print('activity score ', int_act_score[percentuale:-percentuale])
    #print('avg ', avg)
    range = round(avg * 0.25)                       # range -25% + 25%
    #print('range ', range)

    final_hash = []
    final_score = []
    final_time = []
    for index, act_score in enumerate(int_act_score[percentuale:-percentuale]):
        if act_score >= avg-range and act_score <= avg+range:
            final_hash.append(hash_list[percentuale:-percentuale][index])
            final_score.append(int_act_score[percentuale:-percentuale][index])
            final_time.append(time[percentuale:-percentuale][index])
    #print(final_hash, final_score, final_time)

    with open("./final-results/average_commit_" + project_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        for i, value in enumerate(final_hash):
            writer.writerow({csv_headers[0]: final_hash[i],     # Commit_hash
                             csv_headers[1]: final_score[i],    # Commit_ADD_DEL
                             csv_headers[2]: final_time[i]})    # Time
    logger.info(f'Final average Commit: {project_name} ✔')


def average_commit(urls, average_file_type, verbose):
    """ Invoca metodo di analisi: Average Commits """
    # Setting log
    log(verbose)

    # csv header
    csv_headers = ["Commit_hash", "ADD+DEL", "Time"]

    # Indice del repo corrente sotto analisi
    repo_index = 0

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(average_commit) Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits
        if verbose:  # log file + console
            log_view(url, commit.project_name, git.total_commits(), average_file_type, csv_headers)
        else:  # log file
            bar_view(url, commit.project_name, git.total_commits(), average_file_type, csv_headers)
        repo_index += 1

        csv_sort(commit.project_name)   # ordino per ADD+DEL
        csv_avg(commit.project_name, csv_headers)    # calcolo la media

