import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

# Esempio
# path = 'final-results/awesome-docker/sprint_week_master.csv'
main_branch = input("Enter Repository branch folder: final-results/")

path_split = main_branch.split('/')
main_branch_name = path_split[len(path_split)-1]
repo_name = path_split[0]

folder = os.listdir("final-results/" + repo_name)  # returns list
# print("folder ", folder)
# Main branch dati
main_data = pd.read_csv("final-results/" + main_branch)

# Main giorno+anno-settima
tmp_year_week_main = [x[:10] + "-" + str(y) for x, y in zip(main_data['Day'], main_data['Week'])]

# Unisco giorno+anno-settima di tutti i branch con il main: al fine di ottenere un ordinamento cronologico
for branch in folder:
    text_data = pd.read_csv("final-results/" + repo_name + "/" + branch)
    text_week_branch = [x[:10] + "-" + str(y) for x, y in zip(text_data['Day'], text_data['Week'])]
    new_week_day = [week for week in text_week_branch if week not in tmp_year_week_main]  # sprint in branch e non in main
    tmp_year_week_main += new_week_day
tmp_year_week_main.sort()  # ordinamento per data
# print(year_week_main)
tmp_year_week_main = [x[0:4] + "-" + x[len(x) - 2:len(x)] for x in tmp_year_week_main]  # anno-week
# print(year_week_main)
tmp_year_week_main = [x.replace("--", "-") for x in tmp_year_week_main]  # fix week
# print(year_week_main)
year_week_total = list(dict.fromkeys(tmp_year_week_main))  # duplicati
# print("year_week_total ", year_week_total)
# base x del plot complessivo

# Matrice di riferimento per tenere il conto dei sprint commit per branch
matrix_sprint = np.zeros((len(folder), len(year_week_total)), dtype=int)

# Riempio Matrice di sprint con il main.csv: matrix_sprint riga 1 nelle stesse e sole coordinate in cui è presente il
# dato nella stessa data
year_week_main = [x[:4] + "-" + str(y) for x, y in zip(main_data['Day'], main_data['Week'])]
for index, day in enumerate(year_week_main):
    matrix_sprint[0][year_week_total.index(day)] = main_data["Sprint_week"][index]
# print(matrix_sprint)

# Rimozione main branch dal folder
folder.remove(main_branch_name)
# print(folder)

# =====================================

# Commit Main Branch:
# SI LAVORA PER LISTE DI COMMIT PER SINGOLA SETTIMANA!!!
commits_main = main_data["Commits"]

for index, branch in enumerate(folder):
    branch_data = pd.read_csv("final-results/" + repo_name + "/" + branch)  # prendo i dati del branch text
    year_week_branch = [x[:4] + "-" + str(y) for x, y in zip(branch_data['Day'], branch_data['Week'])]  # year_week branch
    commits_branch = branch_data["Commits"]  # prendo i commit del branch-i
    # print(branch)
    for index_day, year_week in enumerate(year_week_branch):
        indice_matrix = year_week_total.index(year_week)  # indice della matrice su cui salvare il dato
        # print("indice_matrix ", indice_matrix)
        if year_week in year_week_main: # se la data è presente nel main branch
            # commit_hash check tra il main e il branch

            # prendo lista commit del main
            commits_main_year_week = commits_main[year_week_main.index(year_week)].split("'") # forse ha senso direttamente index_day
            commits_main_year_week = list(set(commits_main_year_week))
            if ', ' in commits_main_year_week:
                commits_main_year_week.remove(', ')
            commits_main_year_week.remove('[')
            commits_main_year_week.remove(']')
            # print("MAIN: ", commits_main_year_week)

            # prendo lista commit del branch
            commits_branch_year_week = commits_branch[index_day].split("'")
            commits_branch_year_week = list(set(commits_branch_year_week))
            if ', ' in commits_branch_year_week:
                commits_branch_year_week.remove(', ')
            commits_branch_year_week.remove('[')
            commits_branch_year_week.remove(']')
            # print("BARNCH: ", commits_branch_year_week)

            for hash_commit in commits_branch_year_week:        # Stessa settimana
                if hash_commit not in commits_main_year_week:   # commit_Hash diversi
                    # print("DIVERSI")
                    # print(branch, year_week, hash_commit)
                    matrix_sprint[index+1][indice_matrix] += 1
        else:   # data non presente nel MAIN branch
            # print("NUOVO AL MAIN")
            # print(branch, year_week)
            matrix_sprint[index + 1][indice_matrix] = branch_data['Sprint_week'][index_day]

# print(matrix_sprint)

# Define max value limit y-axes
prec_line = np.zeros(len(year_week_total), dtype=int)
for sprint_branch in matrix_sprint:
    prec_line = np.add(prec_line, sprint_branch)
max = max(prec_line)

# Plot
sns.set(style="darkgrid")  # corrisponde al plt.grid(True)
plt.figure(1)

# year_week_total: x asses
# matrix_sprint[0]: main branch
# matrix_sprint[i]: branch folder[i-1]

# Main branch plt
plt.bar(year_week_total, matrix_sprint[0], label=main_branch_name)
# Other branch plt
prec_bottom = np.zeros(len(year_week_total), dtype=int)
for riga, sprint_branch in enumerate(matrix_sprint[1:]):
    prec_bottom = np.add(prec_bottom,matrix_sprint[riga])
    plt.bar(year_week_total, sprint_branch, bottom=prec_bottom, label=folder[riga])
# Y-axes limit top
plt.ylim(0, max+1)
plt.xticks(year_week_total, year_week_total, rotation=90)  # x
plt.xlabel('Weekly commits')  # x
plt.ylabel('Number of changes')  # y
plt.suptitle(repo_name, fontsize=10)
plt.title('Sprint Weekly Stacked Bar Graph', fontsize=15)
plt.legend()
plt.show()