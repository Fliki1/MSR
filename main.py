import argparse
import logging
import git
from giturlparse import parse

# TODO: continuare a seguire la doc di PyDriller ufficiale

from src import WeekCommit, HourCommit, AverageCommit, LastYear_WeekCommit, LineCodeCommit, SprintWeeks, SprintWeeksBoW, LOC

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
        if parse(url).valid & url.endswith(".git"):     # check: git HTTPS
            url_list.append(url)
            logger.info("✔ " + url)
            continue
        else:                                           # check: local repository
            try:
                _ = git.Repo(url).git_dir
                url_list.append(url)
                logger.info("✔ " + url)
            except:
                logger.debug("❌ " + url)                # no git repository
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
    parser = argparse.ArgumentParser(prog='M.S.R.', description="Script che implementa metriche per il M.S.R. : "
                                                                "week_commit , hour_commit, average_commit, ...")
    parser.add_argument("-w", "--week", help="metrica: week commit", action="store_true")
    parser.add_argument("-hrs", "--hour", help="metrica: hour commit", action="store_true")
    parser.add_argument("-avg", "--average", type=str, help="metrica: average commit distribution")
    parser.add_argument("-yr", "--year",  type=str, help="metrica: last year week commit")
    parser.add_argument("-l", "--line", help="metrica: line trend commit", action="store_true")
    parser.add_argument("-s", "--sprint", help="metrica: sprint weeks commit", action="store_true")
    parser.add_argument("-b", "--sprintbow", help="metrica: sprint weeks commit BoW", action="store_true")
    parser.add_argument("-loc", "--lineofcode", help="metrica: andamento LOC nel tempo", action="store_true")
    parser.add_argument("-v", "--verbose", help="restituisce output verboso", action="store_true")
    args = parser.parse_args()
    avg_set = False
    year_set = False
    if (args.average != None):  # Solo per gestire la average_commit
        avg_set = True
    if (args.year == 'True'):     # Solo per gestire last year week commit
        year_set = True
    return args.verbose, args.week, args.hour, avg_set, args.average, args.year, year_set, args.line, args.sprint, args.sprintbow, args.lineofcode


if __name__ == "__main__":
    # Log: gestisce sia la console che il salvataggio dei log [-v] (diversi per modulo)
    verb, week, hour, average, average_file_type, lastyear, current, line, sprint, sprintbow, loc = arg_parse()  # args parse: verbose choise | week commit ?
    log(verb)  # log file

    logger.info('Inizio del M.S.R.')
    urls = get_git_urls()

    if not week and not hour and not average and not lastyear and not line and not sprint and not sprintbow and not loc:  # nessuna opzione scelta: all
        WeekCommit.week_commit(urls, verb)
        HourCommit.hour_commit(urls, verb)
        AverageCommit.average_commit(urls, None, verb)
        LastYear_WeekCommit.last_year_week_commit(urls, current, verb)
        LineCodeCommit.linecode_commit(urls, verb)
        LOC.loc_commit(urls, verb)
        SprintWeeks.sprint_commit(urls, verb)
        SprintWeeksBoW.sprint_commit_bow(urls, verb)
    else:
        if week:
            WeekCommit.week_commit(urls, verb)
        if hour:
            HourCommit.hour_commit(urls, verb)
        if average:
            AverageCommit.average_commit(urls, average_file_type, verb)
        if lastyear:
            LastYear_WeekCommit.last_year_week_commit(urls, current, verb)
        if line:
            LineCodeCommit.linecode_commit(urls, verb)
        if loc:
            LOC.loc_commit(urls, verb)
        if sprint:
            SprintWeeks.sprint_commit(urls, verb)
        if sprintbow:
            SprintWeeksBoW.sprint_commit_bow(urls, verb)

    logger.info('Fine del M.S.R.')
