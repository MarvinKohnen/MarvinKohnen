import csv
import numpy as np
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt

plt.style.use("seaborn-bright")

data = pd.read_csv('/Users/Real/Desktop/Klimaschutz-Bilanz-Muenster-1990-2019_1.csv', sep = ';')
print(data.head(10))

data.loc[0,'Waerme'] = 1121
data.loc[1, 'Waerme'] = 1056
data.loc[2, 'Waerme'] = 1059

ax = plt.gca()
ax.set_ylim([500,1200])


ax.set_facecolor

plt.ylabel('CO\u2082 Ausstoß in kt')
plt.xlabel('Jahr')
x = data['Jahr']
waerme = data['Waerme']
strom = data['Strom']
verkehr = data['Verkehr']
summary = data['Gesamt CO2 in kt']



plt.plot(x, strom)
plt.plot(x, verkehr)
plt.plot(x, waerme)
plt.title('CO\u2082 Ausstoß Münster')
plt.legend(['Strom','Verkehr', 'Wärme'])

plt.show()



