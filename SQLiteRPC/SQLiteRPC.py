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
import thread

def createTimeStamp():
    now = int(time.time())
    temp = time.localtime(now)
    timeStamp = time.strftime("%Y/%m/%d %H:%M:%S", temp)
    return timeStamp

def worker_thread(s, addr):
    try:
        1
    except Exception, ex:
        print ex
    finally:
        if s:
            s.close()


def main():
    print 'sqlite start.'
    while True:
        svr_socket = None
        try:
            socket.setdefaulttimeout(5)
            address = ('127.0.0.1', 6001)  
            svr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
            svr_socket.bind(address)  
            svr_socket.listen(5) 
    
            while True:
                client_socket, client_addr = s.accept()  
                print createTimeStamp()
                print 'connection:',client_addr
                thread.start_new_thread(worker_thread,(client_socket, client_addr))

        except Exception ,ex:
            print ex
            if svr_socket:
                svr_socket.close()
        finally:
            print 'server restart.'
    