#coding=utf-8

import socket
import urllib2, httplib    
import StringIO, gzip
import re
import time
import os

if __name__ == '__main__':
    print 'transmission module.'
    exit()
else:
    print 'load transmission module.'

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
def processOnlinePageList(listArg):
    fp = open('Text.log', 'w+')
    fp.write(createTimeStamp() + '\n')
    conn1 = httplib.HTTPConnection('www.bilibili.com')
    conn2 = httplib.HTTPConnection('api.bilibili.com')
    print 'online list size: %d' % len(listArg)
    for item in listArg:
        videoPageData = processVideoPage(conn1, item[0])
        videoTags = processVideoTag(conn2, item[0])
        #str = '%s :\n%s\n%s\n' % (item, videoPageData, videoTags)
        #item format: uri, tittle, online, other.
        str1 = '[%s]:%s %s\n' % (item[0], item[1], item[7])
        for i in item[2:7]:
            str1 = str1 + '%s ' % (i)
        str1 = str1 + '\n'
        #page data
        str2 = '[Page]:\n'
        if videoPageData:
            for i in videoPageData[0]:
                str2 = str2 + '%s\n' % (i)
            str2 = str2 + 'division\n'
            for i in videoPageData[1]:
                str2 = str2 + '%s ' % (i)
            str2 = str2 + '\n'
        else:
            print 'cannot get video page data.'
        #tags format
        str3 = '[Tags]\n'
        if len(videoTags) > 0:            
            for i in videoTags:
                str3 = str3 + '%s %s %s %s\n' % (i[0], i[1], i[2], i[3])
        else:
            print 'cannot get video tags.'
        s = str1 + str2 + str3
        s.decode('unicode', 'ignore')
        fuck = isinstance(s, unicode)
        fp.write(s)
    conn2.close()
    conn1.close()
    fp.close()

def processVideoData():
    onlinePage = getOnlinePage()
    onlinePageData = None
    if onlinePage:
        onlinePageData = parseOnlinePage(onlinePage[1])
    else:
        print 'can not get online page'
    if onlinePageData:
        processOnlinePageList(onlinePageData)
    else:
        print 'invalid onlinepage data'

#main loop
def mainLoop():
    while True:
        data = getMainPage()