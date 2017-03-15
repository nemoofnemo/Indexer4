import os
import sqlite3
import multiprocessing
import codecs 
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def drawOnlineData():
    dbconn = sqlite3.connect('../data/data201703150922.db')
    cu = dbconn.cursor()
    cu.execute('select * from main_table')
    data = cu.fetchone()
    x = []
    y1 = []
    y2 = []
    while data:
        x.append(data[0])
        y1.append(data[2])
        y2.append(data[3])
        data = cu.fetchone()
    dbconn.commit()
    dbconn.close()
    plt.plot(x, y1, linewidth=1, linestyle="-", label = 'online play')
    plt.plot(x, y2, linewidth=1, linestyle="-", label = 'online user')
    plt.legend(loc='upper left')
    plt.show()

def main():
    drawOnlineData()

if __name__ == '__main__':
    main()