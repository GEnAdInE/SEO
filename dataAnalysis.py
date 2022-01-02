# for the annotation system ref :
# https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-in-matplotlib


# import
import csv
import sys
from pylab import *
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    FilePath = sys.argv[1]
else:
    FilePath = "Empty"


def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False


# class to compile all data
class CurrentData:
    keyword: str  # the keyword
    googleTrend: int  # google trend score
    SEMrsuh: int  # Semrsuh score


ListOfData = []  # Array containing all our CurrentData Object , could be used later if needed
PathIsOk = False
# main code
try:
    while not PathIsOk:
        if yes_or_no("Is this the right path ? : " + FilePath):
            if FilePath.endswith('.csv'):
                PathIsOk = True
            else:
                print("File don't end with a csv\n")
                FilePath = input("Write the new path here : ")
        else:
            FilePath = input("Write the new path here : ")

    print('Reading data wait ! \n')

    with open(FilePath, 'r', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=';')  # opening the csv file containing all data
        for row in reader:
            if len(row) >= 3:  # ignore cases where the data are wrong
                newData = CurrentData()  # Create Object CurrentData
                # gathering the data
                newData.keyword = row[0]
                newData.googleTrend = int(row[1])
                newData.SEMrsuh = int(row[2])
                if newData.SEMrsuh >= 0:  # to not analyze object were we don't have data
                    ListOfData.append(newData)
                print(row)
        file.close()
except:
    print("An error has occurred , please check that the path is right")
    raise

print('All data have been read \n')
print('Processing the data , please wait\n')

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


fig.canvas.mpl_connect("motion_notify_event", hover)  # using a listener
plt.show()  # drawing the plot
