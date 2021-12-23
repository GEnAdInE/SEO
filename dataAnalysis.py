# for the annotation system ref :
# https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-in-matplotlib


# import
import csv
from pylab import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# object


class CurrentData:
    keyword: str
    googleTrend: int
    SEMrsuh: int


ListOfData = []


# main code
with open('Classeur1.csv', 'r', encoding='utf8') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        newData = CurrentData()
        newData.keyword = row[0]
        newData.googleTrend = int(row[1])
        newData.SEMrsuh = int(row[2])
        ListOfData.append(newData)
        print(row)

print('wait')

TrendArray = []
SemRushArray = []
WordArray = []

# putting everything in array is easier when using plot
for word in ListOfData:
    TrendArray.append(word.googleTrend)
    SemRushArray.append(word.SEMrsuh)
    WordArray.append(word.keyword)

# plot parameter
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# create point
sc = ax.scatter(TrendArray, SemRushArray)

# generate the annotation
annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


# function to update annot
def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, Trend: {}, SEO: {}".format("".join([WordArray[n] for n in ind["ind"]]),
                                           "".join(
                                               str([TrendArray[n] for n in ind["ind"]])[1:-1]),
                                           "".join(str([SemRushArray[n] for n in ind["ind"]])[1:-1]))
    print(text)

    annot.set_text(text)

# called on hover event
def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()
