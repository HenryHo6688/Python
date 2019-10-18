#Python Version=3.6
#Coding=utf-8

import socket
import json
import datetime
import random

s = socket.socket()
s.connect(('localhost', 11223))

users = ['henry', 'hens', 'mary', 'rose', 'eric', 'jerry', 'michael']
pages = ['index', 'course', 'pay', 'login']
device = ['macbook', 'iphone', 'ipad']

line = 100
while line>0:
    line = line-1
    temp_time = (datetime.datetime.utcnow()+datetime.timedelta(seconds=random.randint(0, 10))).isoformat()
    data = {'name': random.choice(users), 'visit_time': temp_time, 'device': random.choice(device), 'page': random.choice(pages), 'num': random.randint(0, 10)}
    #s.send(json.dumps(data)+'\r\n')
    dat = json.dumps(data).encode()
    end = ('\r\n').encode()
    s.send(dat+end)
s.close()
