import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# change path all'occorrenza
path = input("Enter CSV Repositories: ")
#path = 'final-results/awesome-docker/sprint_week_master.csv'
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

# Author
plt.figure(2)
plt.bar(datax, data['Authors'])
plt.xticks(datax, datax, rotation=25)     # x
plt.xlabel('Authors per week')        # x
plt.ylabel('Number of authors')     # y
plt.suptitle(path_split[len(path_split) - 1], fontsize=10)
plt.title('Sprint Authors trend', fontsize=15)
plt.show()