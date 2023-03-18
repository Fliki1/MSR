# A suite of Process Metrics to Capture the Effort of Developers
[![it](https://img.shields.io/badge/lang-it-blue)](README.md)

## Details
The project consists of creating a series of specific 
and peculiar metrics to analyze a repository (.git url or local repository)
following the dictates of M.S.R. in order to obtain possible useful information on 
software effort estimation

### 1. Activity per day of the week:
To calculate these values we collected and aggregated (in particular summarized) the commits for each day of the week. 
The metric aims at evaluating the number of commits per day of the week (Mon-Sun).
The aim is to have a graphical representation of the commit
distribution and to identify in which day or in which part of the week they are distributed.
It allows us to determine which are the most labour-intensive days

### 2. Activity per hour of the day:
The metric consists in determining the commit times during the day (0-23). 
This metric shows in which part of the day, we usually have an activity peak and also provides a 
complete snapshot of the daily development activity.
The possible outcomes would be to determine the usual working hours of the development team.

### 3. Average commit distribution:
The metric consists in evaluating the “average” commits of the whole project.
This indicator is calculated starting from each commit activity.
A commit is considered average if its activity
score (sum of the added and eliminated lines) is between -25% and +25%
of the average activity score.
By excluding 10% of samples from both extremities, the mean is calculated on the 80%
of samples which is more accurate. The analysis concerns the evaluation of whether the project over time has a
uniform commit distribution.

It is important to note that what really matter is the frequency of the similar
commits spread in the project, when we find very frequently occurrences, let us
say daily basis, we can state that this project’s activity is stable.

It's possible to specify: `None` to apply the metric to all kind of file or `.py .java .md etc`

### 4. Activity per week since the beginning of the current year:
The metric consists of a weekly vision
of the progress of the last year of the project.
Activity trend on the 52 weeks of a year. 
According to the area in which the project is taking place, the last year could be an intense period for its
completion.
You can choose to analise the last year of the last commit made `False`
or the current nowaday year `True`.


### 5. Lines of code per week:
The metric determines the trend of the overall
source lines of code from the beginning of the project, it is a weekly analysis of
the entire developing of the project but starting from the first commit, in order
to always evaluate the effort trend throughout the program creation phase.

The aim of this metric is to show how development work has been distributed
over the year. It would be possible to recognise the weeks exhibiting intense
work, due to deadlines (e.g. close to release dates) or commits on holiday weeks.

### 6. Lines Of Code in Time:
The metric determines the trend of the overall
source lines of code from the beginning of the project; it analyses the progression
course of LOC in the repository in order to evaluate the important phases in
the development of a project.
This size metric gives the possibility to monitor the program length from time to
time in each commit. The number of lines in the commit files reaches very high
values, especially in reference to a corporate project that had code refactoring
in the long run applied to improve some nonfunctional
features of the software.

The aim of this metric is to show the rate of change of the project size. If
this has been made regularly and in conjunction with what particular events:
code refactoring, integration and adoption of new packages and library, new
development tool that has radically changed the beginning project structure, or
the continuous integration of new feature requests increasing work and effort to
be devoted to project development.

### 7. Sprint week commit trend (Scrum):
The method counts the commits per week and reports the results
over time. The development of a project is divided into weeks of project
progression and weeks of testing, experiments and verification. The possible
metric outcomes want to identify the periods of increased traffic effort against
the periods of lower. The core of the metric is to establish the different latency,
and a possible effort gap during development time, that demonstrates the use of
Scrum Sprint Agile software development processes.
[Sprint_plot.py](Sprint_plot.py) plots the outcomes.


To research and establish the success of the results obtained, 
an automation has been defined. A time window (SLIDING WINDOW) has been created to looking for possible 
Scrums present in the project history.
The goal is to determine and establish thresholds to apply to identify the Scrum that varies from project to project.


Once the window is defined, filters are applied to the collected data in order to satisfy the following assets:
+ the Sprints contained in the time window must be temporally consecutive weeks
+ the Scrums must satisfy the threshold such that the average of the commits 
of the first n-1° weeks must be greater than the next n-th:
`average(n-1)°>n°`
+ do not overlap the sprints with each other

The results of the automatic search for Sprints are reported by [Sprint_plot_Auto.py](Sprint_plot_Auto.py)

### 8. Bag-of-Words Sprint week commit message:
The metric identifies the possible presence of 
an Agile approach: Scrum Sprint. 
The metric is based on the search of Sprint by studying the content of weekly commit messages.
With the aid of the BoW model technique, the presence of keywords such as 
FIX-BUG-DEBUG-DOC-REF-TEST is determined to distinguish 
commits made during the _testing_ phase 
from those made during the _development_ phase of the repository.
The results of the automatic search for Sprints are reported by [Sprint_BoW_plot.py](Sprint_BoW_plot.py)

### Requirements:
[requirements.txt](requirements.txt) includes the list of third-party packages with their respective version numbers

````commandline
pip freeze > requirements.txt
````
* Python 3.8
* Git
* [PyDriller](https://github.com/ishepard/pydriller): a  Python framework that helps developers in analyzing Git repositories
* [giturlparse](https://pypi.org/project/giturlparse/): Parse & rewrite git urls (supports GitHub, Bitbucket, FriendCode, Assembla, Gitlab …)

To run [Sprint_Bow_plot.py](Sprint_BoW_plot.py) the following packages are required:
* **nltk** **stopwords**:
````python
import nltk
nltk.download('stopwords')
````
* **spacy**:
````commandline
python -m spacy download en_core_web_sm
````

### Quick usage:

````commandline
git clone https://github.com/Fliki1/MSR.git
python3 -m venv venv/
source venv/bin/active
pip install -r requirements.txt
````
Start script
````commandline
python main.py [-h] [-w] [-hrs] [-avg AVERAGE] [-yr True/altro] [-l] [-s] [-b] [-v]
````
````commandline
  -h, --help     show this help message and exit
  -w, --week     metric: week commit
  -hrs, --hour   metric: hour commit
  -avg AVERAGE, --average <AVERAGE>   metric: average commit distribution: None | .py | .md etc
  -yr YEAR, --year YEAR   metric: last year week commit
  -l, --line     metric: line trend commit
  -s, --sprint   metric: sprint weeks commit
  -b, --sprintbow   metric: sprint weeks commit BoW
  -v, --verbose  return output verbose
````


## Outcomes 
### 7. Sprint week
The metric is plotted by [Sprint_plot.py](Sprint_plot.py) and [Sprint_plot_Auto.py](Sprint_plot_Auto.py) 
specifying the path where the CSV files are located, inside the folder [Final result](./final-results) or [Data results](./data-results).
The two folders report the results of either the entire repository’s progress or its individual remote branches.
The script generates a series of graphical reports all related to Scrum study.

Start script:
````commandline
python Sprint_plot.py
Enter CSV Repositories: data-results/sprint_week_repositoryname.csv
````

#### Example 1: master banch (Scrum project)
![Screenshot](fig/sprint_branch_es_2.png)

#### Example 2: [maven-web-application-o](https://github.com/yuvaraj3115/maven-web-application-o)
##### Sprint master banch
![Screenshot](fig/maven%20esiti.png)
##### Sprint + values
![Screenshot](fig/maven%20esiti%20+%20esiti.png)
##### Author number
![Screenshot](fig/maven%20autori.png)
##### Sprint + Author
![Screenshot](fig/sprint%20+%20autori.png)
##### Sprint trend on the entire history of the project
![Screenshot](fig/sprint%20week%20+%20no%20commit%20week.png)

Start script:
````commandline
python Sprint_plot_Auto.py
Enter CSV Repositories: data-results/sprint_week_nomerepository.csv
````
##### Scrum Sprint Threshold
![Screenshot](fig/sprint%20auto.png)


### 7.2 Branches Sprint week
The plotting of the branches sprint week metric is done with [Sprint_plot_branch.py](Sprint_plot_branch.py)
specifying the path where the CSV files are located, inside the folder [final-results](final-results).
For the plot of the Branches Sprint week, the execution of metric 7. Sprint week is required
The results are directly visible on the screen.

Start script:
````commandline
python Sprint_plot_branches.py
Enter Repository branch folder: final-results/roposityname/sprint_week_mainbranch.csv
````

#### Branch bar graph
The graph shows the amount of effort of all branches over the sprint week
![Screenshot](fig/Branch%20bar%20graph.png)

#### Percentage branches bar (branches + main)

![Screenshot](fig/branches%20+%20main%20perc%20horiz.png)

#### Percentage branches only
![Screenshot](fig/branches%20horizontal%20perc.png)

#### Percentage main only
Only the percentages of main sprint week branch effort are represented. Sprint week efforts less than 1% are filtered and summed into a single field called Extra in cyan.
![Screenshot](fig/branches%20main%20perc.png)

## Esiti 8. Bow Sprint week
Plot of the BoW Sprint week metric is performed with [Sprint_BoW_plot.py](Sprint_BoW_plot.py).
The script performs the entire BoW process consisting of removing **stopwords** 
from the commit message text, converting the message words to a common domain with the 
**stemming** operation and finally a search for matching of the words we are interested 
in: FIX-BUG-DEBUG-TEST-REF-DOC. Based on their occurrence in commit messages over the course of a week,
they associate a tag with the Sprint they belong to (development or testing).

Start script:
````commandline
python Sprint_BoW_plot.py
Enter CSV Repositories: data-results/sprint_week_namerepository.csv
````
#### BoW plot
The top most used words and top pairs of words in the comments are also reported
![Screenshot](fig/bow.png)


