# M.S.R.
Creazione ex novo del progetto di M.S.R. dei repository in Git. 

Riconversione ed ampliamento del progetto esistente da Java ☕ -> Python 3 🐍

## Details
Il progetto consiste nella creazione di una serie di metriche specifie e peculiari per analizzare, un repository o una lista di questi, seguendo i dettami della M.S.R. al fine di ottenere possibili informazioni utili per l'Ingegneria del Software

## Quick usage
````commandline
python main.py
````


### Requires
[comment]: <> (Pronto prova)
* Python 3.8
* Git
* [PyDriller](https://github.com/ishepard/pydriller): a  Python framework that helps developers in analyzing Git repositories

#### Ambiente di sviluppo
Sto usando PyCharm per gestire un ambiente venv con Python 3.8.
Al fine di prevenire problemi di dependency, rendere il progetto riproducibile e auto-contenuto.
Per installare i dovuti packages su un host che non si hanno i permessi admin.
Evita l'uso della directory `side-packages/` quando si necessità l'uso di questi solo per un progetto.

#### TODO:

1. Esportare i requisiti del progetto e renderli disponibili su git
1. Creare i metodi
1. Vedere se funziona:
````commandline
python3 -m venv venv
source venv/bin/activate
````
E poi installare i requirements:
````commandline
pip install -r requirements.txt
````