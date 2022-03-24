import numpy as np
import pandas as pd
import seaborn as sns
import statistics
import matplotlib.pyplot as plt

# SET:
SLIDING_WINDOW = 4  # 3+1
SCRUM_SEQUENCE = 1  # a partire dalla 1° Sprint lecita, 2°/3°/4°? per poi stabilire le successive

# Esempio
# path = 'data-results/sprint_week_nomerepository.csv'
partial_path = input("Enter CSV Repositories: data-results/sprint_week_")
path = "data-results/sprint_week_" + partial_path

path_split = path.split('/')

data = pd.read_csv(path)  # prendo i dati
sns.set()  # corrisponde al plt.grid(True)

year_week_x = [x[:4] + "-" + str(y) for x, y in zip(data['Day'], data['Week'])]  # dati nella forma anno-settimana

# Ricerca di Sprint validi 3+1
valid_sprint = [] # valid_sprint: Scrum i cuoi sprint soddisfano la soglia: media(1°,2°,3°)>4°
if len(year_week_x) >= SLIDING_WINDOW and len(
        year_week_x) - SLIDING_WINDOW + 1 > 0:  # controllo dimensione dati vs SLIDING_WINDOW
    """print(SLIDING_WINDOW)
    print(len(year_week_x))
    print(len(year_week_x) - SLIDING_WINDOW + 1)"""
    for i in range(len(year_week_x) - SLIDING_WINDOW + 1):
        # soglia media(1°,2°,3°)>4°
        if statistics.mean(data['Sprint_week'][i:i + SLIDING_WINDOW - 1]) > data['Sprint_week'][i + SLIDING_WINDOW - 1]:
            valid_sprint.append(year_week_x[i:i + SLIDING_WINDOW])
            # print(data['Sprint_week'][i:i+SLIDING_WINDOW])
            # print(data['Sprint_week'][i:i+SLIDING_WINDOW-1], " > ", data['Sprint_week'][i+SLIDING_WINDOW-1])
            # print("+1 ", data['Sprint_week'][i+SLIDING_WINDOW-1])
else:
    print("Impossibile ottenere gli sprint: SLIDING_WINDOW > dei dati da analizzare")
    exit(0)


# Check valid sprint to legit sprint: sprint consecutivi settimanali
not_consecutive_sprint = []
for entry in valid_sprint:
    # print(entry)
    year = 0
    day = 0
    for sprint in entry:
        if year == 0 and day == 0:  # set first sprint (1/SLIDINGWINDOW) come parametro di comparazione
            # per i successivi sprint
            year = int(sprint[0:4])
            day = int(sprint[4:].replace('-', ''))
        else:
            # giorno successivo:
            # stesso anno e settimana successiva o anno successivo e settimana 52 prima di settimana 1
            if (year == int(sprint[0:4]) and day + 1 == int(sprint[4:].replace('-', '')) or
                    year + 1 == int(sprint[0:4]) and day == 52 and int(sprint[4:].replace('-', '')) == 1):
                # print("Successivo")
                a = 1  # busy operazione
            else:
                # print("NON Successivo")
                not_consecutive_sprint.append(entry)
                break
            day = int(sprint[4:].replace('-', ''))
            year = int(sprint[0:4])
legit_sprint = [x for x in valid_sprint if x not in not_consecutive_sprint]
# legit_sprint = scrum con sprint consecutivi


# Creazione dei singoli layer di Scrum validati e leciti
def intersection(lst1, lst2):
    """ Return list of common sprint between two list of sprint """
    return list(set(lst1) & set(lst2))


def sprint_sequence(lista, ind):
    """ Return list not-overlap sprint sequence """
    # check se il repositori ha abbastanza elementi per processare almeno 1 scrum
    if ind - 1 < 0:
        return []
    list_return = []
    # Parto dallo sprint di indice indicato: ind
    sprint_overlap = lista[ind - 1]
    list_return.append(sprint_overlap)
    for sprint in lista:
        if len(intersection(sprint_overlap, sprint)) == 0:
            list_return.append(sprint)
            sprint_overlap = sprint
    return list_return


# check se i dati leciti sono abbastanza rispetto alla dimensione della SLIDING_WINDOW
if len(legit_sprint) < SLIDING_WINDOW:
    exit("Impossibile ottenere gli sprint: SLIDING_WINDOW > dati leciti")
# good_sprint_sequence: sequenza di sprint che non si accavallano a partire da SCRUM_SEQUENCE sprint iesimo
good_sprint_sequence = sprint_sequence(legit_sprint, SCRUM_SEQUENCE)
# check
if len(good_sprint_sequence) < 0:
    exit("No abbastanza dati nemmeno per una finestra di Sprint (len(good_sprint_sequence) < 0)")

sprint_develop = np.zeros(len(year_week_x), dtype=int)  # y value of sprint develop
sprint_test = np.zeros(len(year_week_x), dtype=int)  # y value of sprint test
sprint_else = data['Sprint_week'].copy()  # y value of not scrum sprint

for id, year_week in enumerate(year_week_x):
    for sprint in good_sprint_sequence:
        if [True for s in sprint[0:SLIDING_WINDOW - 1] if s == year_week]:
            # print("Developing")
            # print(year_week)
            sprint_develop[id] = data['Sprint_week'][id]
            sprint_else[id] = 0
            break
        if year_week == sprint[SLIDING_WINDOW - 1]:
            # print("Testing", year_week, sprint[SLIDING_WINDOW-1])
            # print(year_week)
            sprint_test[id] = data['Sprint_week'][id]
            sprint_else[id] = 0
            break
"""print(year_week_x)
print(len(sprint_develop))
print(sprint_develop)
print(len(sprint_test))
print(sprint_test)
print(len(sprint_else))
print(sprint_else)"""

# PLOT
plt.figure(1)
barlist_else = plt.bar(year_week_x, sprint_else, color='silver')
barlist_development = plt.bar(year_week_x, sprint_develop, color='cornflowerblue', label='Sprint Development')
barlist_test_fix = plt.bar(year_week_x, sprint_test, color='#ed872d', label='Sprint Test')
plt.legend(loc='upper right')
plt.xticks(year_week_x, year_week_x, rotation=90)  # x
plt.xlabel('Weekly commits')  # x
plt.ylabel('Number of changes')  # y
plt.suptitle('Scrum Sprint Threshold', fontsize=18)
plt.figtext(0.415, 0.9, path_split[len(path_split) - 1], fontsize=14)
plt.show()
