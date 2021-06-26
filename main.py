from pydriller import Repository
from giturlparse import parse
import logging
import argparse

logger = logging.getLogger(__name__)  # nome del modulo corrente


def remove_duplicates(urls):
    """Return list dei urls non duplicati"""
    logger.info('Rimozione url duplicati')
    return list(set(urls))


def check_url(urls):
    """Validate url presi in input, return lista url validi e non duplicati"""
    url_list = []
    urls_not_duplicate = remove_duplicates(urls)  # remove duplicate urls
    for url in urls_not_duplicate:
        if parse(url).valid & url.endswith(".git"):
            url_list.append(url)
            logger.info("✔ " + url)
            # print("✔ "+url)
    logger.info('Urls validati')
    return url_list


def driller(url):
    """Invoca metodo di analisi"""
    # TODO: continuare a seguire la doc di PyDriller ufficiale
    # TODO: prendere spunto da Commit_modificati.py e altro contenuto nella cartella clone ubuntu!
    # TODO: gestire una cartella src/ con i singoli metodi implementati
    for commit in Repository(path_to_repo=url).traverse_commits():
        print('Project {}, Hash {}, author {}'.format(
            commit.project_path,
            commit.hash,
            commit.author.name))


def get_git_urls():
    """Domanda all'user i git da analizzare, return lista url leciti"""
    url_input = input("Enter Gits Repositories: ")
    urls = url_input.split(", ")
    urls_validate = check_url(urls)  # git url ckeck
    return urls_validate


def log(verbos):
    """Setto i parametri per gestire il file di log"""
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    if verbos:
        # StreamHandler: console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # FileHandler: outputfile
    file_handler = logging.FileHandler('./log/main.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def arg_parse():
    """Verifico la possibile chiamata verbose"""
    parser = argparse.ArgumentParser(description="Script che implementa metriche per il M.S.R. : tipo1 ,tipo2...")
    parser.add_argument("-v", "--verbose", help="Restituisce output verboso", action="store_true")
    args = parser.parse_args()
    return args.verbose

'''
def set_log():
    """Setto i parametri per gestire il file di log"""
    # Comprende cosi dal debug ai livelli superiori fino a critical
    # salvo i log nel file (non sovrascrive i old log)
    # Cambio il formato dei log: time - level name - message
    # filemode='w' se si vuole sovrascrivere i log a ogni esecuzione di programma
    # datefmt='%m/%d/%Y %I:%M:%S %p' per cambiare il formato time
    logging.basicConfig(filename='./log/mylog.log', level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info('Started')
    # do something
    logging.info('Finished')
'''

if __name__ == "__main__":
    # Log1
    # set_log()
    # logging.info('Started')
    # dostuff
    # logging.info('Finished')

    # Log2: gestisce sia la console che il salvataggio dei log (diversi per modulo)
    verb = arg_parse()  # args parse: verbose?
    log(verb)           # log file
    logger.info('Inizio')
    urls = get_git_urls()
    # driller(urls)
    logger.info('Fine')
