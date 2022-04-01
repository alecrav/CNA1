#!/usr/bin/python3
#
# Assignment 1
# Enrico Benedettini, Alessandro Cravioglio, Alfio Vavassori 
# https://docs.python.org/3/library/configparser.html

import socket
import sys
import configparser


if len(sys.argv) > 1:
    port_number = int(sys.argv[1])
else:
    port_number = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', port_number))
s.listen(1)


configparser = configparser.ConfigParser()
configFilePath = './vhosts.conf'
configparser.read_file(open(configFilePath))

while True:
    print('Accepting connections')
    conn, addr = s.accept()

    # parse and accept requests
    request = conn.recv(1024).decode()
    print('Request: ' + request)
    request_list = request.split()
    if request_list[0] == 'GET':
        if request_list[1] == '/home.html':
            request_list[1] = '/home.html'
            continue
        if request_list[1] == '/cgi-bin/hello.py':
            conn.send(b'HTTP/1.1 200 OK\r\n\r\nHello World!')
            conn.close()
            continue
        else:
            conn.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
            conn.close()
            continue

    elif request_list[0] == 'PUT':
        print('PUT request')

    elif request_list[0] == 'DELETE':
        # do something
        print("DELETE request")

    elif request_list[0] == 'NTW22INFO':
        print("NTW22INFO request")

    fields = resp.split("\r\n")
    fields = fields[1:] #ignore the GET / HTTP/1.1
    output = {}
    for field in fields:
        key,value = field.split(':')#split each line by http field name and value
        output[key] = value
        
    else:
        print('Unknown request')
        conn.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        

    
# conn.close() HTTP/1.1 ??
s.close()
