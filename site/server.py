#!/usr/bin/python3
#
# Assignment 1
# Enrico Benedettini, Alessandro Cravioglio, Alfio Vavassori 
# https://docs.python.org/3/library/configparser.html

import socket
import sys
from unittest import case
from urllib import response
from zoneinfo import ZoneInfo
from datetime import datetime
from pytz import reference

if len(sys.argv) > 1:
    port_number = int(sys.argv[1])
else:
    port_number = 8083

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', port_number))
s.listen(1)

file = "./site/vhosts.conf"
test = open(file,"r")
lines = test.read()

server = 'Server: Group ComputerNotWorking Server'
names = lines.split('\n')

print(names)

while True:
    print('Accepting connections')
    conn, addr = s.accept()

    # parse and accept requests
    request = conn.recv(1024).decode()
    print('Request: ' + request)
    # Split lines and organize matrix of lines
    request_lines = request.split('\n')
    request_entries = []
    for i in range(len(request_lines)):
        request_entries.append(request_lines[i].split())
    
    # Setting default values
    resp = ""
    version = "HTTP/1.0"
    if (request_entries[0][2]):
        version = request_entries[0][2]
    
    host = ""

    if request_entries[1][1]:
        host = request_entries[1][1]
    
    date = datetime.now().astimezone().strftime("%a, %d %b %Y %H:%M:%S %Z")

    if request_entries[0][0] == "GET":
        
        if request_entries[0][1] ==  "/home.html":
            # do something
            conn.send("/" + host + "/home.html")
            conn.close()
            continue
            # error handling
        
    elif request_entries[0][1] == "PUT":
        print("PUT request")
 
    elif request_entries[0][1] == "DELETE":
        # do something
        print("DELETE request")

    elif request_entries[0][1] == "NTW22INFO":
        admin = ""


        content = "The administrator of " + host + " is " + admin +".\nYou can contact him at "
        content_type = "text/plain"
        length = 0 # TODO - retrieve length of the content

        resp += version + '200 OK\n' + date + '\n' + server + length +  + content
        print("NTW22INFO request")
        conn.send(resp)

    fields = resp.split("\r\n")
    fields = fields[1:] #ignore the GET / HTTP/1.1
    output = {}
    for field in fields:
        key,value = field.split(":")#split each line by http field name and value
        output[key] = value
        # 
    else:
        print("Unknown request")
        conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        # 

    
# conn.close() HTTP/1.1 ??
s.close()
