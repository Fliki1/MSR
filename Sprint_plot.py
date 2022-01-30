import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# change path all'occorrenza
path = input("Enter CSV Repositories: ")
# Esempio
#path = 'final-results/awesome-docker/sprint_week_master.csv'
#oppure path = 'data-results/sprint_week_nomerepository.csv'
path_split = path.split('/')

data = pd.read_csv(path) # prendo i dati
sns.set()   # corrisponde al plt.grid(True)

datax = [x[:4] +"-"+ str(y) for x, y in zip(data['Day'], data['Week'])]     # dati nella forma anno-settimana

# Sprint week
plt.figure(1)
plt.bar(datax, data['Sprint_week'])
plt.xticks(datax, datax, rotation=25)     # x
plt.xlabel('Weekly commits')        # x
plt.ylabel('Number of changes')     # y
plt.suptitle(path_split[len(path_split) - 1], fontsize=10)
plt.title('Sprint Weekly trend [not average]', fontsize=15)
plt.show()

# Author
plt.figure(2)
plt.bar(datax, data['Authors'])
plt.xticks(datax, datax, rotation=25)     # x
plt.xlabel('Authors per week')        # x
plt.ylabel('Number of authors')     # y
plt.suptitle(path_split[len(path_split) - 1], fontsize=10)
plt.title('Sprint Authors trend', fontsize=15)
plt.show()

# Sprint week + Author
plt.figure(3)
plt.bar(datax, data['Sprint_week'])
for index, data_i in enumerate(data['Authors']):    # print valori sopra i bar
    plt.text(x=index, y=0.1, s=f"{data_i}", fontdict=dict(fontsize=18), ha='center', color='white')
            # xaxes, yaxes+1 per uscire dal bar, scritta, font, centrato
plt.xticks(datax, datax, rotation=25)     # x
plt.xlabel('Weekly commits')        # x
plt.ylabel('Number of changes')     # y
plt.suptitle(path_split[len(path_split) - 1], fontsize=10)
plt.title('Sprint Weekly trend [not average] + Count of authors per week', fontsize=15)
plt.show()

# Sprint week Full: conteggia anche le settimane senza commit
#Fill data missing
# Recupero i singoli anni
anni = [x[:4] for x in data['Day']] # prendo solo gli anni dal csv
anni = list(set(anni)) # no duplicati: [2018, 2019, 2020 etc..]
anni.sort()  # necessita di un ordinamento visto che le liste in python cambiano

# Recupero lista delle singole settimane
year_week = [week_i for week_i in range(1, 53)] # lista di 52 entry

# combino settimane e anni
lista_full_data = []
for anno in anni:
    for settimana in year_week:
        lista_full_data.append(str(anno)+'-'+str(settimana))    # unisco i valori secondo lo stesso ordine di datax

# Datax comprendente anche i giorni della settimana senza commit
full_datax = lista_full_data[lista_full_data.index(datax[0]):lista_full_data.index(datax[len(datax)-1])+1]
# restringo la lista, prendendo l'indice del primo valore di datax a noi lecito e l'indice successivo al'ultimo valore lecito di datax, perche' il range funziona cosi

# Sprint commit settimanali + settimane con 0 commit non conteggiate prima
full_sprint = [data['Sprint_week'][datax.index(giorno)] if giorno in datax else 0 for giorno in full_datax]

plt.figure(4)
plt.bar(full_datax, full_sprint)
plt.xticks(full_datax, full_datax, rotation=30)     # x
plt.xlabel('Weekly commits')        # x
plt.ylabel('Number of changes')     # y
plt.suptitle(path_split[len(path_split) - 1], fontsize=10)
plt.title('Sprint Weekly trend [not average]', fontsize=15)
plt.show()

# Join del main branch con un sotto branch: text
text_path = input("Enter CSV Repositories Test to join: ")
text_path_split = text_path.split('/')
text_data = pd.read_csv(text_path) # prendo i dati del branch text

text_datax = [x[:4] +"-"+ str(y) for x, y in zip(text_data['Day'], text_data['Week'])]     # dati nella forma anno-settimana

plt.figure(5)
barlist = plt.bar(datax, data['Sprint_week'])
for indice, valore in enumerate(datax):
    if valore in text_datax:
        barlist[indice].set_color('g')
plt.xticks(datax, datax, rotation=25)     # x
plt.xlabel('Weekly commits')        # x
plt.ylabel('Number of changes')     # y
plt.suptitle(path_split[len(path_split) - 1]+" "+text_path_split[len(text_path_split)-1], fontsize=10)
plt.title('Sprint Weekly trend + selected branch highlight', fontsize=15)
plt.show()
