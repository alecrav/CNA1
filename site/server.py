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

def create_response_by_fields(version, status, status_code, date, server_name, content_length, content_type, content):
    return version+" "+status+" "+status_code+"\nDate: "+date+"\nServer: "+server_name+"\nContent-Length: "+content_length+"\nContent-Type: "+content_type+"\n\n"+content

def string_to_matrix(a, split_by):
    # Split lines and organize matrix of lines
    lines = a.split('\n')
    sections = []
    for i in range(len(lines)):
        sections.append(lines[i].split(split_by))
    return sections

def get_admin_by_name(host, hosts_sections):
    admin_name = ""
    admin_email = ""
    for i in range(len(hosts_sections)):
        if host == hosts_sections[i][0]:
            admin_name = hosts_sections[i][2]
            admin_email = hosts_sections[i][3]
    return "The administrator of " + host + " is " + admin_name +".\nYou can contact him at " + admin_email + "."



if len(sys.argv) > 1:
    port_number = int(sys.argv[1])
else:
    port_number = 8084

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', port_number))
s.listen(1)

test = open("./site/vhosts.conf","r")
lines = test.read()

server_name = 'Server: Group ComputerNotWorking Server'
hosts_sections = string_to_matrix(lines, ",")
print(hosts_sections)

while True:
    print('Accepting connections')
    conn, addr = s.accept()

    # parse and accept requests
    request = conn.recv(1024).decode()
    print('Request: ' + request)
    
    request_entries = string_to_matrix(request," ")
    print(request_entries)
    
    ## Setting default common values
    version = "HTTP/1.0"
    if (request_entries[0][2]):
        version = request_entries[0][2]
    
    host = ""

    if request_entries[1][1]:
        host = request_entries[1][1]
    
    date = datetime.now().astimezone().strftime("%a, %d %b %Y %H:%M:%S %Z")
    ## End of setting default common values


    if request_entries[0][0] == "GET":
        
        if request_entries[0][1] ==  "/home.html":
            # do something
            content = 'content'
            resp = create_response_by_fields(version, '200', 'OK',date,server_name,str(len(content)),content_type,content)
            resp = bytes(resp, 'utf8')
            conn.send(resp)
            conn.close()
            continue
        else:
            resp = bytes((version, '404','NOT FOUND'), 'utf8')
            conn.send(resp)
            conn.close()
            continue
        
    elif request_entries[0][0] == "PUT":
        print("PUT request")

    elif request_entries[0][0] == "DELETE":
        # do something
        print("DELETE request")

    elif request_entries[0][0] == "NTW22INFO":
        print("NTW22INFO request")
        
        content = get_admin_by_name(host, hosts_sections)
        content_type = "text/plain"
        
        resp = create_response_by_fields(version,'200','OK',date,server_name,str(len(content)),content_type,content)

        print(resp)
        resp = bytes(resp, 'utf8')
        conn.send(resp)

    else:
        print("Unknown request")
        conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        # 


    
# conn.close() HTTP/1.1 ??
s.close()