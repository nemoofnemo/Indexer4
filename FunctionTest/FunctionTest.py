import os
import sqlite3
import multiprocessing
import codecs 
import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn as sns
import pickle
import socket

#a = [1,2,3]
#x = pickle.dumps(a)
#print x
#y = pickle.loads(x)
#print y

def worker_thread():
    1

def main():
    address = ('127.0.0.1', 31500)  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
    s.bind(address)  
    s.listen(5) 