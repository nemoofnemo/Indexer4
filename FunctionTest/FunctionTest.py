import os
import sqlite3
import multiprocessing
import codecs 
import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn as sns

dbconn = sqlite3.connect('data20170228.db')
cu = dbconn.cursor()
cu.execute('select * from main_table')
data = cu.fetchall()
dbconn.commit()
dbconn.close()

a = [item[2] for item in data]
plt.plot(a)
b = [item[3] for item in data]
plt.plot(b)
plt.show()

