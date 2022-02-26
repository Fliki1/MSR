import math
import itertools
import pandas as pd
import seaborn as sns
import statistics
import matplotlib.pyplot as plt

SLIDING_WINDOW = 4  # 3+1

# Esempio
# path = 'data-results/sprint_week_nomerepository.csv'
partial_path = input("Enter CSV Repositories: data-results/sprint_week_")
path = "data-results/sprint_week_" + partial_path

path_split = path.split('/')

data = pd.read_csv(path)  # prendo i dati
sns.set()  # corrisponde al plt.grid(True)

# datax = [x[:4] + "-" + str(y) for x, y in zip(data['Day'], data['Week'])]  # dati nella forma anno-settimana

"""# Sprint week
plt.figure(1)
plt.bar(datax, data['Sprint_week'])
plt.xticks(datax, datax, rotation=25)  # x
plt.xlabel('Weekly commits')  # x
plt.ylabel('Number of changes')  # y
plt.suptitle(path_split[len(path_split) - 1], fontsize=10)
plt.title('Sprint Weekly trend [not average]', fontsize=15)
plt.show()"""

year_week_x = [x[:4] + "-" + str(y) for x, y in zip(data['Day'], data['Week'])]  # dati nella forma anno-settimana

valid_sprint = []

# Ricerca di Sprint validi 3+1
if len(year_week_x) >= SLIDING_WINDOW and len(
        year_week_x) - SLIDING_WINDOW + 1 > 0:  # controllo dimensione dati vs SLIDING_WINDOW
    """print(SLIDING_WINDOW)
    print(len(year_week_x))
    print(len(year_week_x) - SLIDING_WINDOW + 1)"""
    for i in range(len(year_week_x) - SLIDING_WINDOW + 1):
        # soglia media(1°,2°,3°)>4°
        if statistics.mean(data['Sprint_week'][i:i + SLIDING_WINDOW - 1]) > data['Sprint_week'][i + SLIDING_WINDOW - 1]:
            valid_sprint.append(year_week_x[i:i + SLIDING_WINDOW])
            # lecit_sprint.append(data['Sprint_week'][i:i+SLIDING_WINDOW].tolist())    # salvo 3+1 converto da series to list)

            # print(data['Sprint_week'][i:i+SLIDING_WINDOW])
            # print(data['Sprint_week'][i:i+SLIDING_WINDOW-1], " > ", data['Sprint_week'][i+SLIDING_WINDOW-1])
            # print("+1 ", data['Sprint_week'][i+SLIDING_WINDOW-1])
else:
    print("Impossibile ottenere gli sprint: SLIDING_WINDOW > dei dati da analizzare")

# print(valid_sprint)

# Check valid sprint to legit sprint: sprint consecutivi settimanali
not_consecutive_sprint=[]
for entry in valid_sprint:
    print(entry)
    year = 0
    day = 0
    for sprint in entry:
        if year == 0 and day == 0:  # set first sprint (1/SLIDINGWINDOW) come parametro di comparazione
                                    # per i successivi sprint
            year = int(sprint[0:4])
            day = int(sprint[4:].replace('-', ''))
        else:
            # giorno successivo:
            # stesso anno e settimana successiva o anno successivo e settimana 1 settimana 52
            if (year == int(sprint[0:4]) and day+1 == int(sprint[4:].replace('-', '')) or
                year+1 == int(sprint[0:4]) and day == 52 and int(sprint[4:].replace('-', '')) == 1 ):
                print("Successivo")
                """print(year, "==", sprint[0:4], "?")
                y = int(day) + 1
                print(y, "==", sprint[4:].replace('-', ''), "?")"""
            else:
                print("NON Successivo")
                """print(year, "==", sprint[0:4], "?")
                y = int(day) + 1
                print(y, "==", sprint[4:].replace('-', ''), "?")"""
                not_consecutive_sprint.append(entry)
                break
            day = int(sprint[4:].replace('-', ''))
            year = int(sprint[0:4])
list_difference = [x for x in valid_sprint if x not in not_consecutive_sprint]
print(list_difference)



"""if year == sprint[0:4] and day+1 == int(sprint[4:].replace('-', '')):
    print("Consecutivi")
    print(year, day)
    print(sprint[0:4], sprint[4:].replace('-', ''))"""

"""def intersection(lst1, lst2):
    #lst3 = [list(filter(lambda x: x in lst1, sublist)) for sublist in lst2]
    return list(set(lst1) & set(lst2))

coppie = []
for entry_1 in lecit_sprint:
    for entry_2 in [y for y in lecit_sprint if y is not entry_1]:
        if len(intersection(entry_1, entry_2)) == 0:
            coppie.append([entry_1, entry_2])
print(coppie)"""

# Calcolo la dimensione massima di sprint possibili in un repo.
"""print(len(year_week_x))
print(SLIDING_WINDOW)
print(math.floor(len(year_week_x)/SLIDING_WINDOW))
print("#sprint validi ",len(lecit_sprint))

all_combinations = []
combinations_object = itertools.combinations(lecit_sprint, math.floor((len(year_week_x)/SLIDING_WINDOW)/2))
combinations_list = list(combinations_object)
all_combinations += combinations_list
print(len(all_combinations))"""

"""# Join del main branch con un sotto branch: text
partial_text_path = input("Enter CSV Repositories Test to join: final-results/")
text_path = "final-results/" + partial_text_path
text_path_split = text_path.split('/')
text_data = pd.read_csv(text_path)  # prendo i dati del branch text

text_datax = [x[:4] + "-" + str(y) for x, y in
              zip(text_data['Day'], text_data['Week'])]  # dati nella forma anno-settimana

plt.figure(5)
barlist = plt.bar(datax, data['Sprint_week'])
for indice, valore in enumerate(datax):
    if valore in text_datax:
        barlist[indice].set_color('g')
plt.xticks(datax, datax, rotation=25)  # x
plt.xlabel('Weekly commits')  # x
plt.ylabel('Number of changes')  # y
plt.suptitle(path_split[len(path_split) - 1] + " " + text_path_split[len(text_path_split) - 1], fontsize=10)
plt.title('Sprint Weekly trend + selected branch highlight', fontsize=15)
plt.show()"""
