#coding=utf-8

import re
import socket
import httplib 
import time
import Transmission
import os
import sqlite3
import multiprocessing
import codecs 

if __name__ == '__main__':
    while True:
        try:
            Transmission.mainLoop()
        except Exception, ex:
            print ex
        print 'program crashed.program will restart in 300sec.'
        time.sleep(300)

#def daemon():
#    while True:
#        try:
#            Transmission.mainLoop()
#        except Exception, ex:
#            print ex
#        print 'program crashed.program will restart in 300sec.'
#        time.sleep(300)

#def main():
#    while True:
#        print '[daemon process start]'
#        Transmission.TICK_COUNT = int(time.time())
#        p = multiprocessing.Process(name = 'daemon',target = daemon)
#        p.daemon = True
#        p.start()
#        while True:
#            now = int(time.time())
#            timeStamp = Transmission.createTimeStamp()
#            if now - Transmission.TICK_COUNT > 720:
#                p.terminate()
#                print 'program chrash.'
#                fp = codecs.open('warning.log', 'a+', 'utf-8')
#                fp.write('%s %d -> program crashed.' % (timeStamp, now))
#                fp.close()
#                break
#            time.sleep(725)
    
#if __name__ == '__main__':
#    print '[program start]'    
#    main()