import argparse
import logging

from giturlparse import parse

# TODO: continuare a seguire la doc di PyDriller ufficiale
# TODO: prendere spunto da Commit_modificati.py e altro contenuto nella cartella clone ubuntu!

from src import WeekCommit

# create logger
logger = logging.getLogger(__name__)  # nome del modulo corrente (main.py): global logger

def remove_duplicates(urls):
    """ Return list dei urls non duplicati """
    logger.info('Rimozione url duplicati')
    return list(set(urls))


def check_url(urls):
    """ Validate url presi in input, return lista url validi e non duplicati """
    url_list = []
    for url in urls:
        if parse(url).valid & url.endswith(".git"):
            url_list.append(url)
            logger.info("✔ " + url)
        else:   # evitabile questo else
            logger.debug("❌ " + url)
    logger.info('Urls validati')
    return url_list


def get_git_urls():
    """ Domanda all'user i git da analizzare, return lista url leciti """
    url_input = input("Enter Gits Repositories: ")
    urls = url_input.split(", ")
    urls_not_duplicate = remove_duplicates(urls)  # remove duplicate urls
    urls_validate = check_url(urls_not_duplicate)  # git url ckeck
    return urls_validate

def log(verbos):
    """ Setto i parametri per gestire il file di log """
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    if verbos:
        # create console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    # FileHandler: outputfile
    file_handler = logging.FileHandler('./log/main.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def arg_parse():
    """ Verifico la possibile chiamata verbose """
    parser = argparse.ArgumentParser(description="Script che implementa metriche per il M.S.R. : week_commit ,tipo2...")
    parser.add_argument("-w", "--week", help="metrica: week commit", action="store_true")
    parser.add_argument("-v", "--verbose", help="restituisce output verboso", action="store_true")
    args = parser.parse_args()
    return args.verbose, args.week
    # TODO: gestione chiamata di quale tipo di metrica si vuole eseguire


if __name__ == "__main__":

    # Log: gestisce sia la console che il salvataggio dei log [-v] (diversi per modulo)
    verb, week = arg_parse()  # args parse: verbose choise?
    log(verb)           # log file
    logger.info('Inizio del M.S.R.')
    urls = get_git_urls()
    # if week:
    WeekCommit.week_commit(urls, verb)
    logger.info('Fine del M.S.R.')
