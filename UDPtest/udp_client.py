#coding=utf-8

from socket import *

HOST = '123.206.62.174'
PORT = 6001
BUFSIZ = 4096
ADDR = (HOST, PORT)

#创建客户端UDP套接字
udpClient = socket(AF_INET, SOCK_DGRAM)

while True:
    data = raw_input('>')
    if not data:
        break
    #向服务器端发送数据
    udpClient.sendto(data,ADDR)
    #接收来自服务器端的数据
    data, ADDR = udpClient.recvfrom(BUFSIZ)
    print(data)
    if not data:
        break

udpClient.close()
