#coding=utf-8

import socket
import urllib2, httplib    
import StringIO, gzip
import re

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

#main page

def getMainPage():
    conn = httplib.HTTPConnection("www.bilibili.com")
    conn.request("GET", "/") 
    response = conn.getresponse()
    data = response.read()
    data = unicode(data, 'utf-8')
    conn.close()
    return (response, data)

def parseMainPage(data):
    pattern = re.compile(R'<a href="/video/online\.html" title="[\u4e00-\u9fa5]*?.*?(\d+)" target="_blank">.*?<em>(\d+)</em></a>', re.M);
    ret = pattern.search(data)
    if ret:
        print ret.groups()  
        return ret.groups()   
    else:
        print ('0','0')
        return ('0','0')

#online page

def getOnlinePage():
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
    conn.close()
    return (response, data)

def parseOnlinePage(data):
    pattern = re.compile(R'<div class="ebox" typeid=".*?"><a href="(.*?)" title="(.*?)" target="_blank"><img src="(.*?)"/><p class="etitle">(.*?)</p></a><div class="dlo"><span class="play"><i class="b-icon b-icon-v-play"></i>(.*?)</span><span class="dm"><i class="b-icon b-icon-v-dm"></i>(.*?)</span><span class="author">(.*?)</span></div><p class="ol"><b>(.*?)</b>.*?</p></div>', re.M);
    ret = pattern.findall(data)
    print ret
    return ret

def processVideoPage(conn, uri): 
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
    #second, parse data by regex exp
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
    return (retData1, retData2)

def processOnlinePageList(listArg):
    conn = httplib.HTTPConnection('www.bilibili.com')
    print processVideoPage(conn, '/video/av8680746/')   
    conn.close()