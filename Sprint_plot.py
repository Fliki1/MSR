import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# change path all'occorrenza
data = pd.read_csv('final-results/awesome-docker/sprint_week_master.csv') # prendo i dati
sns.set()   # corrisponde al plt.grid(True)

datax = [x[:4] +"-"+ str(y) for x, y in zip(data['Day'], data['Week'])]     # dati nella forma anno-settimana

plt.figure(1)
plt.bar(datax, data['Sprint_week'])
plt.xticks(datax, datax, rotation=20)     # x
plt.xlabel('Weekly commits')        # x
plt.ylabel('Number of changes')     # y
plt.suptitle('sprint_week_master.csv', fontsize=10)
plt.title('Sprint Weekly trend [not average]', fontsize=15)
plt.show()