import csv
from pylab import *
import numpy as np
import matplotlib.pyplot as plt


class CurrentData:
    keyword: str
    dataPoint: list


ListOfData = []

with open('TEST-DATA.csv', 'r', encoding='utf8') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        tmplist = row[1]
        tmplist = tmplist[1:-1]
        tmplist = tmplist.split(',')
        newData = CurrentData()
        newData.keyword = row[0]
        newData.dataPoint = [float(i) for i in tmplist]
        ListOfData.append(newData)
        print(row)

print('wait')
test = ListOfData[0].dataPoint
test = test[0:60]
somme = 0+0
i=0
for num in test:
    somme += num
    test[i] = num/100
    i += 1
print(somme)

plt.plot(test)
plt.show()
