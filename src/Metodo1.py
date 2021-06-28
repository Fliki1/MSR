from src import ProgressionBar
from pydriller import Repository
from pydriller import Git
import time

#TODO: settare un file di log anche qui

def metodo2(urls):
    """Invoca metodo di analisi"""
    for url in urls:
        repo = Repository(path_to_repo=url).traverse_commits()
        commit = next(repo)
        git = Git(commit.project_path)
        print(git.total_commits())
        for commit in ProgressionBar.progressBar(Repository(path_to_repo=url).traverse_commits(), git.total_commits(), prefix='Progress:', suffix='Complete', length=50):
            # TODO: o file di log o progression bar, non entrambi insieme
            print('Hash {}'.format(commit.hash))
            time.sleep(0.1)



# TODO: rimuovere metodo(urls) solo quando si è sicuri di farlo
def metodo(urls):
    # A List of Items
    items = list(range(0, 57))

    # A Nicer, Single-Call Usage
    for item in ProgressionBar.progressBar(items, prefix='Progress:', suffix='Complete', length=50):
        # print('Hash {}'.format(commit.hash))
        time.sleep(0.1)
