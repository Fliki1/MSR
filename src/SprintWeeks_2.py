import csv
import time
import logging
import os
from src import ProgressionBar
from pydriller import Repository
from pydriller import Git
from git import Repo

logger = logging.getLogger(__name__)  # nome del modulo corrente (SprintWeeks.py)


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
    file_handler = logging.FileHandler('./log/SprintLog.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def bar_view(repo, repo_name, total_commits, csv_headers):
    """ Sprint Weeks: bar console, non buono per benchmark visto il 0.1s di delay """
    author = []
    with open("./main_data-results/sprint_week_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        week_commit = 0
        prec_commit = None
        for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                                 prefix='Progress:', suffix='Complete', length=50):

            logger.info(f'Hash: {commit.hash}, '
                        f'Week: {commit.committer_date.isocalendar()[1]}, '
                        f'Time: {commit.committer_date}, '
                        f'Author: {commit.author.email}')

            if prec_commit == None:
                prec_commit = commit
                week_commit = week_commit + 1
                author.append(commit.author.email)
                continue

            # conteggio commit della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                    prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                week_commit = week_commit + 1
                if commit.author.email not in author:
                    author.append(commit.author.email)
            else:   # cambio di settimana salvo gli esiti
                writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Time
                                 csv_headers[1]: week_commit,  # Commit della settimana
                                 csv_headers[2]: prec_commit.committer_date.isocalendar()[1],  # Week
                                 csv_headers[3]: len(author)})  # Authors
                week_commit = 1     # reset
                author = []
                author.append(commit.author.email)
            prec_commit = commit
            time.sleep(0.1)
        # last commit
        writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Time
                         csv_headers[1]: week_commit,  # Commit della settimana
                         csv_headers[2]: prec_commit.committer_date.isocalendar()[1],  # Week
                         csv_headers[3]: len(author)})  # Authors
    logger.info(f'Sprint Week: {repo_name} ✔')


def log_view(repo, repo_name, csv_headers):
    """ Sprint Weeks: log console """
    author = []
    with open("./main_data-results/sprint_week_" + repo_name + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        week_commit = 0
        prec_commit = None
        for commit in Repository(path_to_repo=repo).traverse_commits():

            logger.info(f'Hash: {commit.hash}, '
                        f'Week: {commit.committer_date.isocalendar()[1]}, '
                        f'Time: {commit.committer_date}, '
                        f'Author: {commit.author.email}')

            if prec_commit == None:  # Forse senza if e prec_commit = commit standard a ogni ciclo
                prec_commit = commit
                week_commit = week_commit + 1
                author.append(commit.author.email)
                continue

            # conteggio dei commit: della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                    prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                week_commit = week_commit + 1
                if commit.author.email not in author:
                    author.append(commit.author.email)
            else:  # cambio di settimana salvo gli esiti
                writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Time
                                 csv_headers[1]: week_commit,  # Commit della settimana
                                 csv_headers[2]: prec_commit.committer_date.isocalendar()[1],  # Week
                                 csv_headers[3]: len(author)})  # Authors
                week_commit = 1     # reset
                author = []
                author.append(commit.author.email)
            prec_commit = commit
        # last commit
        writer.writerow({csv_headers[0]: prec_commit.committer_date,  # Time
                         csv_headers[1]: week_commit,  # Commit della settimana
                         csv_headers[2]: prec_commit.committer_date.isocalendar()[1],  # Week
                         csv_headers[3]: len(author)})  # Authors
    logger.info(f'Sprint Week: {repo_name} ✔')


def branch_view(repo, branch, repo_name, total_commits, csv_branch):
    """ Sprint Weeks: bar console, non buono per benchmark visto il 0.1s di delay """
    if not os.path.exists("./final-results/"+repo_name):
        os.makedirs("./final-results/"+repo_name)
    branch_name = branch.split('/')     # take only the name of branch
    author = []
    with open("./final-results/"+repo_name+"/sprint_week_" + branch_name[len(branch_name) - 1] + ".csv", 'w') as f:
        # Header del csv
        writer = csv.DictWriter(f, fieldnames=csv_branch)
        writer.writeheader()
        week_commit = 0
        prec_commit = None
        hash_commit_week = []
        for commit in ProgressionBar.progressBar(
                Repository(path_to_repo=repo, only_in_branch=branch, only_no_merge=False).traverse_commits(),
                total_commits, prefix='Progress:', suffix='Complete', length=50):

            logger.info(f'Hash: {commit.hash}, '
                        f'Week: {commit.committer_date.isocalendar()[1]}, '
                        f'Time: {commit.committer_date}, '
                        f'Author: {commit.author.email}')

            if prec_commit == None:
                prec_commit = commit
                week_commit = week_commit + 1
                author.append(commit.author.email)
                hash_commit_week.append(commit.hash)
                continue

            # conteggio commit della stessa settimana nello stesso anno
            if prec_commit.committer_date.year == commit.committer_date.year and \
                    prec_commit.committer_date.isocalendar()[1] == commit.committer_date.isocalendar()[1]:
                week_commit = week_commit + 1
                hash_commit_week.append(commit.hash)
                if commit.author.email not in author:
                    author.append(commit.author.email)
            else:   # cambio di settimana salvo gli esiti
                writer.writerow({csv_branch[0]: prec_commit.committer_date,  # Day
                                 csv_branch[1]: week_commit,  # Commit della settimana
                                 csv_branch[2]: prec_commit.committer_date.isocalendar()[1],  # Week
                                 csv_branch[3]: len(author),
                                 csv_branch[4]: hash_commit_week})  # Authors
                week_commit = 1     # reset
                author = []
                hash_commit_week = []
                author.append(commit.author.email)
                hash_commit_week.append(commit.hash)
            prec_commit = commit
            time.sleep(0.1)
        # last week
        writer.writerow({csv_branch[0]: prec_commit.committer_date,  # Day
                         csv_branch[1]: week_commit,  # Commit della settimana
                         csv_branch[2]: prec_commit.committer_date.isocalendar()[1],  # Week
                         csv_branch[3]: len(author),
                         csv_branch[4]: hash_commit_week})  # Authors
    logger.info(f'Sprint Week Branch {branch}: {repo_name} ✔')


def sprint_commit(urls, verbose):
    """ Invoca metodo di analisi: Sprint Week Commits """
    # Setting log
    log(verbose)

    # csv header
    csv_headers = ["Day", "Sprint_week", "Week", "Authors", "Commits"]

    # Indice del repo corrente sotto analisi
    repo_index = 0

    # Invocazione console/bar per ogni repo corrispettivo
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')  # project name
        print(f'(sprint_week_all_commit) Project: {commit.project_name}')

        # Repo info
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')  # total commits

        # Sprint in all repo
        if verbose:  # log file + console
            log_view(url, commit.project_name, csv_headers)
        else:  # log file
            bar_view(url, commit.project_name, git.total_commits(), csv_headers)

        # Sprint in all Branch
        r = Repo(commit.project_path)
        remote_refs = r.remote().refs

        index = 1
        # scan remote branches
        for refs in remote_refs:
            branch_name = refs.name.split('/')
            if branch_name[len(branch_name) - 1] == 'HEAD':  # evito l'analisi del branch HEAD, solitamente punta master
                continue
            print(f'(sprint_week_branch_commit) Project: {commit.project_name} Branch: {refs.name} '
                  f'#: {index}/{len(remote_refs)-1}')
            len_branch = len(list(Repository(path_to_repo=url, only_in_branch=refs.name).traverse_commits()))
            branch_view(url, refs.name, commit.project_name, len_branch, csv_headers)
            index += 1

        # next repo
        repo_index += 1

# TODO: calcolare la media! dagli esiti stessi?
