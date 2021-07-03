from src import ProgressionBar
from pydriller import Repository
from pydriller import Git
import time
import logging

logger = logging.getLogger(__name__)  # nome del modulo corrente (main.py): global logger

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
    file_handler = logging.FileHandler('./log/Metodo1.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def bar_view(repo, total_commits):
    """ Metodo1 bar console, non buono per benchmark visto il 0.1sec di delay """
    for commit in ProgressionBar.progressBar(Repository(path_to_repo=repo).traverse_commits(), total_commits,
                                             prefix='Progress:', suffix='Complete', length=50):
        logger.info('Hash {}'.format(commit.hash))
        time.sleep(0.1)

def log_view(repo, total_commits):
    """ Metodo1 log console """
    commit_count = 1
    for commit in Repository(path_to_repo=repo).traverse_commits():
        logger.info(f'{commit_count}/{total_commits}: Hash {commit.hash}')
        commit_count = commit_count + 1


def metodo2(urls, verbose):
    """ Invoca metodo di analisi """
    log(verbose)
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        logger.info(f'Project: {commit.project_name}')
        print(f'Project: {commit.project_name}')
        git = Git(commit.project_path)
        logger.debug(f'Project: {commit.project_name} #Commits: {git.total_commits()}')
        if verbose: # log file + console
            log_view(url, git.total_commits())
        else:   # log file
            bar_view(url, git.total_commits())
