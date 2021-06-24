import test
from pydriller import Repository

def driller(url):
    # TODO: come ottenere la lista di commit di un repository
    # TODO: continuare a seguire la doc di PyDriller ufficiale
    # TODO: prendere spunto da Commit_modificati.py e altro contenuto nella cartella clone ubuntu!
    # TODO: gestire una cartella src/ con i singoli metodi implementati
    for commit in Repository(path_to_repo=url).traverse_commits():
        print('Project {}, Hash {}, author {}'.format(
            commit.project_path,
            commit.hash,
            commit.author.name))

def main():
    # codice da testare o di default variabili settate
    print("ciao a tutti faccio cose")
    # posso richiamare altri metodi come metodo()... metodo() che se viene fatto l'import di main in un altro scritp potrà essere eseguito
    #test.print_hi("pippo")
    #test.function()

if __name__ == "__main__":
    # execute only if run as a script
    # se eseguito come main script di tutto il progetto, stabilisco condizioni di base: repository fissato, quali metodi ecc..
    #main()
    # TODO: gestire più url da input
    url = ["https://github.com/ishepard/pydriller.git"]
    driller(url)