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
cu.execute("insert into test values(7,'%s')" % u'\\asdf')
print cu.fetchall()
cx.commit()
cu.close()
cx.close()
