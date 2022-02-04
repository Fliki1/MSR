import pandas as pd
import csv
import spacy
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

data = pd.read_csv(path)  # prendo i dati
data = data[pd.notnull(data['Msg_data'])]  # checking not missing msg
print(data.head(10))


def clean_text(text):
    text = BeautifulSoup(text, "lxml").text  # HTML decoding
    text = text.lower()  # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub(' ', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(parola for parola in text.split() if parola not in STOPWORDS)  # delete stopwords from text
    return text


data['Msg_data'] = data['Msg_data'].apply(clean_text)
print(data['Msg_data'][0])

# ---------------

# stemming e salvataggio su file
stemmer = PorterStemmer()

# csv header
csv_headers = ["Day", "Week", "Msg_data"]

with open("testset.csv", 'w') as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
    for i, line in enumerate(data['Msg_data']):
        word_str = ""
        for word in line.split():
            word_str += stemmer.stem(word) + " "
        writer.writerow({'Day': data['Day'][i], 'Week': data['Week'][i], 'Msg_data': word_str})
f.close()

# ---------------
data = pd.read_csv("testset.csv")
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
fieldnam = ['repo_name', 'commit_hash', 'Tag']

with open("finale.csv", 'w') as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
f.close()

for index, row in data.iterrows():
    sentence = nlp(row['Msg_data'])
    print(sentence)
    phrase_matches = m_tool(sentence)
    for match_id, start, end in phrase_matches:
        string_id = nlp.vocab.strings[match_id] # Get string representation: 'FIX'
        span = sentence[start:end] # The matched span
        if span.text:
            with open("finale.csv", 'a') as f:
                writer = csv.DictWriter(f, fieldnames=csv_headers)
                writer.writerow({'Day': row['Day'], 'Week': row['Week'], 'Msg_data': string_id})
            f.close()
