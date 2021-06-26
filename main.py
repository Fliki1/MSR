# import test
from pydriller import Repository
from giturlparse import parse

def remove_duplicates(urls):
    """Return list dei urls non duplicati"""
    return list(set(urls))

def check_url(urls):
    """Validate url presi in input, return lista ulr validi e non duplicata"""
    url_list = []
    urls_not_duplicate = remove_duplicates(urls)    # remove duplicate urls
    for url in urls_not_duplicate:
        if(parse(url).valid & url.endswith(".git")):
            url_list.append(url)
            print("✔ "+url)
    return url_list

def driller(url):
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
    #print(urls)
    urls_validate = check_url(urls) # git url ckeck
    return urls_validate

if __name__ == "__main__":
    # execute only if run as a script
    # se eseguito come main script di tutto il progetto, stabilisco condizioni di base: repository fissato, quali metodi ecc..
    #main()
    urls = get_git_urls()
    #print(urls)
    driller(urls)
