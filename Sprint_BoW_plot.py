import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import spacy
import seaborn as sns
from spacy.matcher import Matcher
import nltk
from nltk.stem.porter import *
import re
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

# nltk.download('stopwords')
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

# change path all'occorrenza
path = input("Enter CSV Repositories: ")
# Esempio
# path = 'final-results/awesome-docker/sprint_week_master.csv'
# oppure path = 'data-results/sprint_week_nomerepository.csv'
path_split = path.split('/')

data_sprint = pd.read_csv(path)  # prendo i dati
data_sprint = data_sprint[pd.notnull(data_sprint['Msg_data'])]  # checking not missing msg
#print(data.head(10))


def clean_text(text):
    text = BeautifulSoup(text, "lxml").text  # HTML decoding
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub(' ', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(parola for parola in text.split() if parola not in STOPWORDS)  # delete stopwords from text
    return text


data_sprint['Msg_data'] = data_sprint['Msg_data'].apply(clean_text)
#print(data['Msg_data'][0])

# ---------------

# stemming e salvataggio su file
stemmer = PorterStemmer()

# csv header
csv_headers = ["Day", "Week", "Msg_data"]

with open("testset.csv", 'w') as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
    for i, line in enumerate(data_sprint['Msg_data']):
        word_str = ""
        for word in line.split():
            word_str += stemmer.stem(word) + " "
        writer.writerow({'Day': data_sprint['Day'][i], 'Week': data_sprint['Week'][i], 'Msg_data': word_str})
f.close()

# ---------------
data_sprint = pd.read_csv("testset.csv")
nlp = spacy.load('en_core_web_sm')

m_tool = Matcher(nlp.vocab)

fix = [[{"LOWER": "fix"}],
       [{"TEXT": {"REGEX": "^fix"}}]]

test = [[{"LOWER": "test"}],
       [{"TEXT": {"REGEX": "^test"}}]]

bug = [[{"LOWER": "bug"}],
       [{"TEXT": {"REGEX": "^bug"}}]]

refactoring = [[{"LOWER": "refact"}],
       [{"TEXT": {"REGEX": "^refact"}}]]

feature = [[{"LOWER": "feature"}],
       [{"TEXT": {"REGEX": "^feature"}}]]

documentation = [[{"LOWER": "documentation"}],
       [{"TEXT": {"REGEX": "^documentation"}}]]

m_tool.add('FIX', fix, on_match=None)
m_tool.add('TEST', test, on_match=None)
m_tool.add('BUG', bug, on_match=None)
m_tool.add('REF', refactoring, on_match=None)
m_tool.add('FEAT', feature, on_match=None)
m_tool.add('DOC', documentation, on_match=None)

# Header del csv
fieldnam = ['Day', 'Week', 'Tag']

with open("finale.csv", 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnam)
    writer.writeheader()
f.close()

for index, row in data_sprint.iterrows():
    sentence = nlp(row['Msg_data'])
    phrase_matches = m_tool(sentence)
    for match_id, start, end in phrase_matches:
        string_id = nlp.vocab.strings[match_id] # Get string representation: 'FIX'
        span = sentence[start:end] # The matched span
        if span.text:
            with open("finale.csv", 'a') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnam)
                writer.writerow({'Day': row['Day'], 'Week': row['Week'], 'Tag': string_id})
            f.close()

# -----------------------
# bow + tag count
data_count = pd.read_csv('finale.csv')

data_count_head = ["Day", "Week", "Tag", "#Tag"]

week_grouped = data_count.groupby(["Day", "Week"])["Tag"].value_counts()
with open("bow_tag.csv", 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data_count_head)
    writer.writeheader()
f.close()

bow = pd.DataFrame(week_grouped)
bow.to_csv("bow_tag.csv", header=False, mode="a")

# -----------------------
# bow tag filter multiple tag sprint to a single tag

data_count_filter = pd.read_csv('bow_tag.csv')

with open("bow_tag_filter.csv", 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data_count_head)
    writer.writeheader()
    for i, line in enumerate(data_count_filter['Day']):  # ciclo sui giorni
        if i == 0:
            prec = line
            max_index = i
            continue
        if prec == line:   # giorni uguali con tag diversi
            #print(i, "uguali: ", prec, " - ", line)
            if data_count_filter['#Tag'][i-1] < data_count_filter['#Tag'][i]:
                prec = line
                max_index = i
        else:   # diversi salvo il precedente
            #print(i, "diversi: ", prec, " - ", line, " salvo")
            writer.writerow({'Day': data_count_filter['Day'][max_index], 'Week': data_count_filter['Week'][max_index],
                             'Tag': data_count_filter['Tag'][max_index], '#Tag': data_count_filter['#Tag'][max_index]})
            prec = line
            max_index = i

        if i == len(data_count_filter['Day'])-1:  # devo salvare l'ultimo
            # print(i, "ultimo")
            #if data_count_filter['Day'][i] != data_count_filter['Day'][i-1]:  # se diverso dal penultimo - salvo
            writer.writerow({'Day': data_count_filter['Day'][max_index], 'Week': data_count_filter['Week'][max_index],
                         'Tag': data_count_filter['Tag'][max_index], '#Tag': data_count_filter['#Tag'][max_index]})
f.close()

os.remove('testset.csv')
os.remove('finale.csv')
os.remove('bow_tag.csv')

# ----------------
# Join scrum con gli sprint derivati dal BoW tag

data_bow = pd.read_csv("bow_tag_filter.csv")  # prendo i dati bow

# richiedo i dati del main scrum sprint
main_path = input("Enter CSV Repositories Main to join: ")
text_path_split = main_path.split('/')
main_data = pd.read_csv(main_path) # prendo i dati del branch text

main_datax = [x[:4] +"-"+ str(y) for x, y in zip(main_data['Day'], main_data['Week'])]     # dati nella forma anno-settimana
datab = [x[:4] +"-" + str(y) for x, y in zip(data_bow['Day'], data_bow['Week'])]

sns.set()   # corrisponde al plt.grid(True)

plt.figure(1)
barlist = plt.bar(main_datax, main_data['Sprint_week'])
for indice, valore in enumerate(main_datax):
    if valore in datab:
        print("dentro ",data_bow[datab.index(valore)])
        if data_bow[datab.index(valore)] in ['FIX', 'TEST', 'BUG', 'REF', 'DOC']:
            barlist[indice].set_color('g')
plt.xticks(main_datax, main_datax, rotation=25)     # x
plt.xlabel('Weekly commits')        # x
plt.ylabel('Number of changes')     # y
plt.suptitle(path_split[len(path_split) - 1], fontsize=10)
plt.title('Sprint Weekly trend BoW', fontsize=15)
plt.show()
