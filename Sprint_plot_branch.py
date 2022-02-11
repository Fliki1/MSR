import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Esempio
# path = 'final-results/awesome-docker/sprint_week_master.csv'
main_branch = input("Enter Repository branch folder: final-results/")

path_split = main_branch.split('/')
main_branch_name = path_split[len(path_split)-1]
repo_name = path_split[0]

folder = os.listdir("final-results/" + repo_name)  # returns list

# Main branch dati
main_data = pd.read_csv("final-results/" + main_branch)
sns.set()  # corrisponde al plt.grid(True)

# Main giorno+anno-settima
year_week_main = [x[:10] + "-" + str(y) for x, y in zip(main_data['Day'], main_data['Week'])]

# Unisco giorno+anno-settima di tutti i branch con il main: al fine di ottenere un ordinamento cronologico
for branch in folder:
    text_data = pd.read_csv("final-results/" + repo_name + "/" + branch)
    text_week_branch = [x[:10] + "-" + str(y) for x, y in zip(text_data['Day'], text_data['Week'])]
    new_week_day = [week for week in text_week_branch if week not in year_week_main]  # sprint in branch e non in main
    year_week_main += new_week_day
year_week_main.sort()  # ordinamento per data
#print(year_week_main)
year_week_main = [x[0:4] + "-" + x[len(x)-2:len(x)] for x in year_week_main]  # anno-week
#print(year_week_main)
year_week_main = [x.replace("--", "-") for x in year_week_main]  # fix week
#print(year_week_main)
year_week_main = list(dict.fromkeys(year_week_main))  # duplicati
print(year_week_main)
# base x del plot complessivo

"""# Commit Main Branch:
# SI LAVORA PER LISTE DI COMMIT PER SINGOLA SETTIMANA!!!
commits_main = main_data["Commits"]

# prendo i dati di un secondo branch
print('=========')
text_data = pd.read_csv("final-results/" + path_split[0] + "/" + folder[0])  # prendo i dati del branch text

# Commits del branch text
data_filtrare = text_data["Commits"][0].split("'")
data_filtrare = list(set(data_filtrare))
print(data_filtrare)
data_filtrare.remove('[')
data_filtrare.remove(']')
data_filtrare.remove(', ')
print(data_filtrare)"""

"""

text_datax = [x[:4] + "-" + str(y) for x, y in
              zip(text_data['Day'], text_data['Week'])]  # dati nella forma anno-settimana

plt.figure(5)
barlist = plt.bar(data_x, main_data['Sprint_week'])
for indice, valore in enumerate(data_x):
    if valore in text_datax:
        barlist[indice].set_color('g')
plt.xticks(data_x, data_x, rotation=25)  # x
plt.xlabel('Weekly commits')  # x
plt.ylabel('Number of changes')  # y
plt.suptitle(path_split[len(path_split) - 1] + " " + text_path_split[len(text_path_split) - 1], fontsize=10)
plt.title('Sprint Weekly trend + selected branch highlight', fontsize=15)
plt.show()
"""