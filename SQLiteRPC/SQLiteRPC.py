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
import time

def worker_thread():
    1

def main():
    while True:
        try:
            socket.setdefaulttimeout(5)
            address = ('127.0.0.1', 6001)  
            svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
            svr_socket.bind(address)  
            svr_socket.listen(5) 
    
            while True:
                ss, addr = s.accept()  
                print 'connection:',addr

        except Exception ,ex:
            print ex
    