#coding=utf-8

import re
import socket
import httplib 
import time
import Transmission
import os
import sqlite3
    
if __name__ == '__main__':
    print '[program start]'    
else:
    print 'program is not a module.'
    exit()

while True:
    try:
        Transmission.mainLoop()
    except Exception, ex:
        print ex
    print 'program crashed.program will restart in 300sec.'
    time.sleep(300)