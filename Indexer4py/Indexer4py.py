#coding=utf-8

import re
import socket
import httplib 
import time
import Transmission
import os
import sqlite3
    
if __name__ == '__main__':
    print 'program start.'    
else:
    print 'program is not a module.'
    exit()

#Transmission.mainLoop()

cx = sqlite3.connect('data.db')
cu = cx.cursor()
cu.execute("insert into test values(4, '%s')" % '你好')
cx.commit()
cu.execute('select * from test')
print cu.fetchall()
cu.close()
cx.close()