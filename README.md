# M.S.R.
Creazione ex novo del progetto di M.S.R. dei repository in Git. 

Riconversione ed ampliamento del progetto esistente da Java ☕ -> Python 3 🐍

## Details
Il progetto consiste nella creazione di una serie di metriche 
specifie e peculiari per analizzare, un repository o una lista
di questi (.git url e local repository), seguendo i dettami 
della M.S.R. al fine di ottenere possibili informazioni utili 
per l'Ingegneria del Software


### 1. Activity per day of the week:
To calculate these values we collected and aggregated (in particular summarized) the commits for each day of the week. The goal is to have a graphical representation of the commit
distribution and to identify in which day or in which part of the week it is.

### 2. Activity per hour of the day:
Similar to the previous one, in this case, the commit data are distributed throughout the hours of the day. 
This metric shows in which part of the day, we usually have an activity peak and also provides a complete snapshot of the daily development activity.

### 3. Average commit distribution:
This indicator is calculated starting from each commit activity.
When we refer to commit activity, we mean all additions
and deletions every commit contains; the sum of these two
parameters is the "activity score" of the commit.
By excluding 10% of samples from both extremities, the mean is calculated on the 80%
of samples which is more accurate. Starting from this average value we consider all
the commits that have an activity score included between -25% and +25% of the previusly average value.

### 4. Activity per week since the beginning of the current year:
In this case we retrieve the week trend commit data for the current year or the last year of the project.
Activity trend on the 52 weeks of a year.

### 5. Lines of code per week:
The lines of code metric shows the number of lines for every week. 
This indicator is very useful to study the evolution of the project as it highlights the
development phases and helps defining the adopted methodology, from the beginning to the end of project.

### 6. Sprint week commit trend:
Metrica per individuare la possibile presenza di un 
approccio Agile: Scrum Sprint, che il team di sviluppo 
software ha adottato sul singolo repository.
Ciascuna delle Sprint sono costituite essenzialmente da 3 
settimane impiegate allo sviluppo +1 dedicata al Testing.
La ricerca viene effettuata sia sullo storico del repository in totale
che sui singoli branch che lo costituiscono.
La metrica si basa sulla ricerca e report di questa finestra temporale
con relative conclusioni.

_I dati raccolti NON riportano la media, ma il count settimale dei commit._

_Nota: la metrica Sprint non conteggia e non riporta le settimane senza commit._

### Requires
[comment]: <> (Pronto prova)
* Python 3.8
* Git
* [PyDriller](https://github.com/ishepard/pydriller): a  Python framework that helps developers in analyzing Git repositories
* [giturlparse](https://pypi.org/project/giturlparse/): Parse & rewrite git urls (supports GitHub, Bitbucket, FriendCode, Assembla, Gitlab …)
#### Requirements:
requirements.txt comprende la lista delle third party packages con i relativi version numbers
````commandline
pip freeze > requirements.txt
````
Per eseguire [] si richiedono il download delle seguenti package:
* Per nltk **stopwords**:
````commandline
import nltk
nltk.download('stopwords')
````
* Per **spacy**:
````commandline
python -m spacy download en_core_web_sm
````

## Quick usage:
Git clone
````commandline
git clone https://github.com/Fliki1/MSR.git
````
Creare un nuovo ambiente venv nella directory desiderata
````commandline
python3 -m venv venv/
````
Installare le dipendeze del progetto dentro una virtual enviroment attiva
````commandline
source venv/bin/active
pip install -r requirements.txt
````
Start script
````commandline
python main.py [-h] [-w] [-hrs] [-avg AVERAGE] [-yr True/altro] [-l] [-v]
````
````commandline
  -h, --help     show this help message and exit
  -w, --week     metrica: week commit
  -hrs, --hour   metrica: hour commit
  -avg AVERAGE, --average AVERAGE   metrica: average commit distribution
  -yr YEAR, --year YEAR             metrica: last year week commit
  -l, --line     metrica: line trend commit
  -s, --sprint   metrica: sprint weeks commit
  -v, --verbose  restituisce output verboso
````

#### Ambiente di sviluppo
Sto usando PyCharm per gestire un ambiente venv con Python 3.8.
* Al fine di prevenire problemi di dependency, rendere il progetto riproducibile e auto-contenuto.
* Per installare i dovuti packages su un host che non si hanno i permessi admin.
* Evita l'uso della directory `side-packages/` quando si necessità l'uso di questi solo per un progetto.

## Esiti Sprint week
Plot della metrica Sprint week effettuato con [Sprint_plot.py](Sprint_plot.py) specificando il path dove sono presenti i CSV file, dentro la cartella [Final result](./final-results) o [Data results](./data-results).
Le due cartelle riportano gli esisti rispettivamente di tutto l'andamento del repository o dei singoli branch che lo caratterizzano.
Lo script esegue una serie di report grafici tutti vincolati allo studio dello Scrum:
* numero andamento commit negli sprint
* andamento sprint nel corso degli anni
* numero autori degli sprint
* combinazione di sprint su branch diversi: feature vs test

Start script
````commandline
python Sprint_plot.py
Enter CSV Repositories: data-results/sprint_week_nomerepository.csv
````

#### Esempio 1: master branch

![Screenshot](fig/sprint_branch_es_1.png)

#### Esempio 2: master banch
![Screenshot](fig/sprint_branch_es_2.png)

#### Esempio 3: [maven-web-application-o](https://github.com/yuvaraj3115/maven-web-application-o)
##### Sprint
![Screenshot](fig/maven%20esiti.png)
##### Sprint + valori commit per settimana
![Screenshot](fig/maven%20esiti%20+%20esiti.png)
##### Autori
![Screenshot](fig/maven%20autori.png)
##### Sprint + Autori
![Screenshot](fig/sprint%20+%20autori.png)
##### Sprint nell'intero storico attuale del progetto
![Screenshot](fig/sprint%20week%20+%20no%20commit%20week.png)
##### Main branch + sotto branch (es: testing)
![Screenshot](fig/main_branch_join_branch.png)

#### TODO:

1. Vedere se funziona:
````commandline
python3 -m venv venv
source venv/bin/activate
````
E poi installare i requirements:
````commandline
pip install -r requirements.txt
````
