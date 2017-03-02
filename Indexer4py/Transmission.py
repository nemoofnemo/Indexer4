#coding=utf-8

import socket
import urllib2, httplib    
import StringIO, gzip
import re
import time
import os
import codecs 
import json
import sqlite3

#if __name__ == '__main__':
#    print 'transmission module.'
#    exit()
#else:
#    print '[load transmission module]'

def gzdecode(data) :  
    compressedstream = StringIO.StringIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    data2 = gziper.read() 
    return data2   

def createTimeStamp():
    now = int(time.time())
    temp = time.localtime(now)
    timeStamp = time.strftime("%Y/%m/%d %H:%M:%S", temp)
    return timeStamp

#main page

def getMainPage():
    conn = None
    ret = None
    try:
        conn = httplib.HTTPConnection("www.bilibili.com")
        conn.request("GET", "/") 
        response = conn.getresponse()
        data = response.read()
        data = unicode(data, 'utf-8')
        ret = (response, data)
    except Exception, ex :
        print ex
    finally:
        if conn:
            conn.close()
    return ret

def parseMainPage(data):
    pattern = re.compile(R'<a href="/video/online\.html" title="[\u4e00-\u9fa5]*?.*?(\d+)" target="_blank">.*?<em>(\d+)</em></a>', re.M);
    ret = pattern.search(data)
    if ret: 
        return ret.groups()   
    else:
        return None

#online page

def getOnlinePage():
    ret = None
    conn = None
    try:
        conn = httplib.HTTPConnection('www.bilibili.com')
        conn.request('GET', '/video/online.html', '', {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Referer':'http://www.bilibili.com/','Accept-Language':'zh-CN,zh;q=0.8', 'Accept-Encoding':'gzip'}) 
        response = conn.getresponse()
        data = response.read()
        headers = response.getheaders()
        if headers.count( ('Content-Encoding', 'gzip') ) == True :
            data = gzdecode(data)
        if headers.count( ('content-encoding', 'gzip') ) == True :
            data = gzdecode(data)
        data = unicode(data, 'utf-8')
        ret = (response, data)
    except Exception , ex:
        print ex
    finally:
        if conn:
            conn.close()
    return ret

#return video list
def parseOnlinePage(data):
    pattern = re.compile(R'<div class="ebox" typeid=".*?"><a href="(.*?)" title="(.*?)" target="_blank"><img src="(.*?)"/><p class="etitle">(.*?)</p></a><div class="dlo"><span class="play"><i class="b-icon b-icon-v-play"></i>(.*?)</span><span class="dm"><i class="b-icon b-icon-v-dm"></i>(.*?)</span><span class="author">(.*?)</span></div><p class="ol"><b>(.*?)</b>.*?</p></div>', re.M);
    ret = pattern.findall(data)
    return ret

#return ( (1,2,3), (1,2,3) )
def processVideoPage(conn, uri): 
    results = None
    try:
        #first, get html page
        conn.request('GET', uri, '', {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Accept-Language':'zh-CN,zh;q=0.8', 'Accept-Encoding':'gzip'}) 
        response = conn.getresponse()
        data = response.read()
        headers = response.getheaders()
        if headers.count( ('Content-Encoding', 'gzip') ) == True :
            data = gzdecode(data)
        if headers.count( ('content-encoding', 'gzip') ) == True :
            data = gzdecode(data)
        data = unicode(data, 'utf-8')
        #second, keywords,desc,author,catgory?
        pattern = re.compile(R'<meta name="keywords" content="(.*?)" />.*?<meta name="description" content="(.*?)" />.*?<meta name="author" content="(.*?)" />', re.M | re.S)
        ret1 = pattern.search(data)   
        retData1 = () 
        if ret1:
            retData1 = ret1.groups()
        pattern = re.compile(R'"tminfo" xmlns:v="//rdf\.data-vocabulary\.org/#".*?<a href="(.*?)".*?>(.*?)</a>.*?<a href=\'(.*?)\'.*?>(.*?)</a>.*?<a href="(.*?)".*?>(.*?)</a>', re.M | re.S)
        ret2 = pattern.search(data)
        retData2 = ()
        if ret2:
            retData2 = ret2.groups()
        results = (retData1, retData2)
    except Exception , ex:
        print ex
    finally:
        1 
    return results

#return list
def processVideoTag(conn, uri):
    ret = []
    try:
        pattern = re.compile(R'/video/av(\d+)/', re.M | re.S)
        ma = pattern.match(uri)
        aid = ''
        if ma:
            aid = ma.group(1)
        else:
            return ret
        uri = 'http://api.bilibili.com/x/tag/archive/tags?aid=' + aid + '&jsonp=jsonp'
        #get data
        conn.request('GET', uri, '', {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Accept-Language':'zh-CN,zh;q=0.8', 'Accept-Encoding':'gzip'}) 
        response = conn.getresponse()
        data = response.read()
        headers = response.getheaders()
        if headers.count( ('Content-Encoding', 'gzip') ) == True :
            data = gzdecode(data)
        if headers.count( ('content-encoding', 'gzip') ) == True :
            data = gzdecode(data)
        data = unicode(data, 'utf-8')
        pattern = re.compile(R'{"tag_id":(.*?),"tag_name":"(.*?)".*?"content":"(.*?)".*?"ctime":(.*?),.*?}', re.M | re.S)
        ret = pattern.findall(data)
    except Exception , ex:
        print ex
    finally:
        1   
    return ret

#return list:
#video page data, video tags

def writeVideoDataToDB(dbconn, index, listitem, videoPageData, videoTags):
    cu = None
    try:
        cu = dbconn.cursor()

        cu.execute('select max(video_id) from video_table')
        video_id = 1
        ret = cu.fetchone()[0]
        if ret:
            video_id = ret + 1            

        cu.execute('select max(keyword_id) from keyword_table')
        keyword_id = 1
        ret = cu.fetchone()[0]
        if ret:
            keyword_id = ret + 1

        cu.execute('select max(division_id) from division_table')
        division_id = 1
        ret = cu.fetchone()[0]
        if ret:
            division_id = ret + 1

        keyword_index = video_id
        division_index = video_id
        keywords = []
        division = []

        if videoPageData and len(videoPageData[0]) == 0 and len(videoPageData[1]) == 0:
            desc = u'bilibili番剧'
            keywords.append(u'番剧')
            division = [u'http://bangumi.bilibili.com/22/',u'番剧',u'http://bangumi.bilibili.com/22/',u'番剧']
        elif videoPageData:
            desc = videoPageData[0][1]
        else:
            print 'invalid video pagedata in writeVideoDataToDB:1'
            desc = u' '        

        #video table
        play_count_str = '0'
        if listitem[4] != '--':
            play_count_str = listitem[4]
        if videoPageData:
            cu.execute("insert into video_table values(%d,%d,'%s','%s','%s','%s',%s,%s,'%s',%s,%d,'%s',%d)" % (video_id, index, listitem[0],listitem[1],listitem[2],listitem[3],play_count_str,listitem[5],listitem[6],listitem[7],keyword_index,desc,division_index))
        
        #tags
        try:
            for i in videoTags:
                keywords.append(i[1])
                cu.execute('select tag_id from tag_table where tag_id = %s' % i[0])
                if len(cu.fetchall()) == 0:
                    cu.execute("insert into tag_table values(%s,'%s','%s',%s)" % (i[0],i[1],i[2],i[3]))
        except Exception , ex:
            #do nothing
            1

        #div    
        if videoPageData and len(videoPageData[1]) != 0:
            for i in videoPageData[1][2:]:
                division.append(i)
            if len(videoPageData[1]) == 6:
                if videoPageData[1][3] not in keywords:
                    keywords.append(videoPageData[1][3])
                if videoPageData[1][5] not in keywords:
                    keywords.append(videoPageData[1][5])
        try:
            cu.execute("insert into division_table values(%d,%d,'%s','%s','%s','%s')" % (division_id, division_index, division[0],division[1],division[2],division[3]))
        except Exception , ex:
            #do nothing
            1        
        
        #keyword
        if videoPageData and len(videoPageData[0]) == 3:
            temp = videoPageData[0][0].split(u',')
            for i in temp:
                if i not in keywords:
                    keywords.append(i)
        try:
            for i in keywords:
                cu.execute("insert into keyword_table values(%d,%d,'%s')" % (keyword_id,keyword_index,i))
                keyword_id = keyword_id + 1
        except Exception , ex:
            #do nothing
            1
        dbconn.commit()
    except Exception , ex:
        print ex
    finally:
        if cu:
            cu.close()


def processOnlinePageList(listArg, dbconn, index):
    conn1 = None
    conn2 = None
    try:
        #fp = codecs.open('text.txt', 'a+', 'utf-8')
        conn1 = httplib.HTTPConnection('www.bilibili.com')
        conn2 = httplib.HTTPConnection('api.bilibili.com')
        print '[Info]:online list size: %d' % len(listArg)

        for item in listArg:
            videoPageData = processVideoPage(conn1, item[0])
            videoTags = processVideoTag(conn2, item[0])
            #write to db
            writeVideoDataToDB(dbconn, index, item, videoPageData, videoTags)

    except Exception , ex:
        print ex
    finally:
        conn2.close()
        conn1.close()

def processVideoData(dbconn, index):
    onlinePage = getOnlinePage()
    onlinePageData = None
    if onlinePage:
        onlinePageData = parseOnlinePage(onlinePage[1])
    else:
        print 'can not get online page'
    if onlinePageData:
        processOnlinePageList(onlinePageData, dbconn, index)
    else:
        print 'invalid onlinepage data'

#lives

#return list
def getLiveList():
    results = []
    conn = None
    try:
        conn = httplib.HTTPConnection('live.bilibili.com')
        conn.request('GET', 'http://live.bilibili.com/area/home?area=subject&order=online&cover=1', '', {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Referer':'http://www.bilibili.com/','Accept-Language':'zh-CN,zh;q=0.8', 'Accept-Encoding':'gzip'}) 
        response = conn.getresponse()
        data = response.read()
        headers = response.getheaders()
        if headers.count( ('Content-Encoding', 'gzip') ) == True :
            data = gzdecode(data)
        if headers.count( ('content-encoding', 'gzip') ) == True :
            data = gzdecode(data)  
        data = data.decode('raw_unicode_escape')
        #get list
        pattern = re.compile(R'{"roomid":(.*?),"short_id":(.*?),"uid":(.*?),"uname":"(.*?)",.*?"title":"(.*?)",.*?"online":(.*?),"area":(.*?),"areaName":"(.*?)","link":"(.*?)","stream_id":(.*?),.*?}', re.M | re.S)
        results = pattern.findall(data)
    except Exception , ex:
        print ex
    finally:
        if conn:
            conn.close()
    return results

def processLivePage(conn, uri):
    results = None
    try:      
        conn.request('GET', '/' + uri , '', {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','Referer':'http://www.bilibili.com/','Accept-Language':'zh-CN,zh;q=0.8', 'Accept-Encoding':'gzip'}) 
        response = conn.getresponse()
        data = response.read()
        headers = response.getheaders()
        if headers.count( ('Content-Encoding', 'gzip') ) == True :
            data = gzdecode(data)
        if headers.count( ('content-encoding', 'gzip') ) == True :
            data = gzdecode(data)
        data = unicode(data, 'utf-8')
        #get data
        pattern = re.compile(R'<meta name="keywords" content="(.*?)">.*?<meta name="description".*?content="(.*?)".*?>', re.DOTALL)
        temp = pattern.search(data)
        ret1 = ()
        if temp:
            ret1 = temp.groups()
        pattern = re.compile(R'<div class="live-tag v-top" title=".*?">(.*?)</div>', re.M | re.S)
        ret2 = pattern.findall(data)
        results = (ret1, ret2)
    except Exception , ex:
        print ex
    finally:
        1
    return results

def writeLiveDataToDB(dbconn, index, listitem, livePageData):
    cu = None
    try:
        cu = dbconn.cursor()
        
        cu.execute('select max(live_id) from live_table')
        live_id = 1
        ret = cu.fetchone()[0]
        if ret:
            live_id = ret + 1

        cu.execute('select max(live_tag_id) from live_tag_table')
        live_tag_id = 1
        ret = cu.fetchone()[0]
        if ret:
            live_tag_id = ret + 1

        cu.execute('select max(keyword_id) from keyword_table')
        keyword_id = 1
        ret = cu.fetchone()[0]
        if ret:
            keyword_id = ret + 1

        keyword_index = keyword_id
        live_tag_index = live_tag_id

        keywords = []

        #live table
        cu.execute("insert into live_table values(%d,%d,%s,%s,%s,'%s','%s',%s,%s,'%s','%s','%s',%d,%d)" % (live_id, index, listitem[0], listitem[1], listitem[2], listitem[3], listitem[4], listitem[5], listitem[6], listitem[7], listitem[8], listitem[9], keyword_index, live_tag_index))

        #tags
        try:
            if livePageData:
                for i in livePageData[1]:
                    keywords.append(i)
                    cu.execute("insert into live_tag_table values(%d, %d, '%s')" % (live_tag_id, live_tag_index, i))
                    live_tag_id = live_tag_id + 1
        except Exception , ex:
            #do nothing
            1

        #division
        if listitem[7] not in keywords:
            keywords.append(listitem[7])        

        #keywords
        try:
            for i in keywords:
                cu.execute("insert into keyword_table values(%d,%d,'%s')" % (keyword_id,keyword_index,i))
                keyword_id = keyword_id + 1
        except Exception , ex:
            #do nothing
            1
        dbconn.commit()
    except Exception , ex:
        print ex
    finally:
        if cu:
            cu.close()

def processLiveList(dbconn, index):
    liveList = getLiveList()    
    print '[Info]:live list size: %d' % len(liveList)
    if len(liveList) > 0:
        conn = None
        try:
            conn = httplib.HTTPConnection('live.bilibili.com')
            ret = None

            for item in liveList:
                if item[1] != u'0':
                    ret = processLivePage(conn, item[1])
                elif item[1] == u'0':
                    ret = processLivePage(conn, item[0]) 
                else:
                    print 'invalid room id'
                    continue

                #write to db
                writeLiveDataToDB(dbconn, index, item, ret)

                if ret == None:
                    print 'invalid LivePage return value'
                    continue
        except Exception, ex:
            print ex
        finally:
            if conn:
                conn.close()
    else:
        print 'cannot get live list.'
    
#main loop

def writeMainTable(dbconn, index, timeStamp, playCount, onlineCount):
    cu = None
    try:
        cu = dbconn.cursor()
        cu.execute("insert into main_table values(%d,'%s',%s,%s)" % (index, timeStamp, playCount, onlineCount))
        dbconn.commit()
    except Exception , ex:
        print ex
    finally:
        if cu:
            cu.close()

def clearTable():
    dbconn = sqlite3.connect('data.db')
    cu = dbconn.cursor()
    cu.execute('DELETE FROM main_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM video_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM keyword_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM tag_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM live_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM live_tag_table')
    cu.execute('VACUUM')
    cu.execute('DELETE FROM division_table')
    cu.execute('VACUUM')
    dbconn.commit()
    cu.close()
    dbconn.close()

#monitor value
TICK_COUNT = 0

def mainLoop():
    #start indexer
    global TICK_COUNT
    socket.setdefaulttimeout(5)
    
    while True:                
        print '---------------------------------------'
        #get database        
        timeStamp = createTimeStamp()
        index = int(time.time())
        TICK_COUNT = index
        dbconn = sqlite3.connect('data.db')
        
        print '[%s]: indexer start.Index = %d' % (timeStamp, index)
        data = getMainPage()
        MainPageData = parseMainPage(data[1])
        if MainPageData:
            temp = '[TimeStamp]:%s\n[Index]:%d\n[Online]:%s %s' % (timeStamp, index, MainPageData[0], MainPageData[1])
            print temp
            #write to db
            writeMainTable(dbconn, index, timeStamp, MainPageData[0], MainPageData[1])            
        else:
            print 'cannot get main page data, abort operation.'
            continue

        processVideoData(dbconn, index)
        processLiveList(dbconn, index)
        dbconn.commit()
        dbconn.close()
        print '[Indexer]: %s -> done.' % createTimeStamp()

        #break
        time.sleep(300)