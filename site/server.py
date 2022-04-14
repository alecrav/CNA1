#!/usr/bin/python3
#
# Assignment 1
# Enrico Benedettini, Alessandro Cravioglio, Alfio Vavassori 
# https://docs.python.org/3/library/configparser.html

import socket
import sys
from urllib import response
from datetime import datetime

def create_response_by_fields(version, status, status_code, date, server_name, content_length, content_type, content):
    return version+" "+status+" "+status_code+"\nDate: "+date+"\nServer: "+server_name+"\nContent-Length: "+content_length+"\nContent-Type: "+content_type+"\n\n"+content

def string_to_matrix(a, split_by, request):
    # Split lines and organize matrix of lines
    lines = a.split('\n')
    sections = []
    for i in range(len(lines)):
        if request and i == 0:
            sections.append(lines[i].split())
        elif lines[i] != "":
            sections.append(lines[i].split(split_by))
    return sections

def request_to_dictionary(a):
    sections_matrix = string_to_matrix(a,':',True)
    sections_dictionary = {}
    sections_dictionary["Method"] = sections_matrix[0][0]
    sections_dictionary["Path"] = sections_matrix[0][1]
    sections_dictionary["Version"] = sections_matrix[0][2]

    for i in range(1,len(sections_matrix)):
        print("Request line "+str(i)+":")
        print(sections_matrix[i])
        print("  ")
        value = sections_matrix[i][1]
        value = value.split()[0]
        field = sections_matrix[i][0]
        sections_dictionary[field] = value # Adding the field to the dictionary
    return sections_dictionary

def hosts_to_dictionary(a):
    hosts_entries_matrix = string_to_matrix(a,',',False)
    hosts_entries_dictionary = {}
    for i in range(len(hosts_entries_matrix)):
        hosts_entries_dictionary[hosts_entries_matrix[i][0]] = hosts_entries_matrix[i][1:4]
    return hosts_entries_dictionary

def get_content_by_name(host, hosts_sections):
    fields = hosts_sections[host][0]
    return "The administrator of " + host + " is " + fields[1] +".\nYou can contact him at " + fields[2] + "."



if len(sys.argv) > 1:
    port_number = int(sys.argv[1])
else:
    port_number = 8090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', port_number))
s.listen(1)

test = open("./site/vhosts.conf","r")
lines = test.read()

server_name = 'Server: Group ComputerNotWorking Server'
hosts_sections = hosts_to_dictionary(lines)
print(hosts_sections)

not_found_response = b"HTTP/1.1 404 Not Found\r\n\r\n"
malformed_respones = b"HTTP/1.1 400 Bad Request\r\n\r\n"

while True:
    print('Accepting connections')
    conn, addr = s.accept()

    # parse and accept requests
    request = conn.recv(1024).decode()
    print('Request: ' + request)
    
    request_entries = request_to_dictionary(request)
    

    ## Setting default common values    
    date = datetime.now().astimezone().strftime("%a, %d %b %Y %H:%M:%S %Z")

    if len(request_entries) < 2 or (not request_entries["Host"]) or (not request_entries["Version"]):
        conn.send(malformed_respones)
    else:
        host = request_entries["Host"]
        version = request_entries["Version"]
        ## End of setting default common values
        
        if request_entries["Method"] == "GET":
            
            print (request_entries["Path"])
            if request_entries["Path"] == "/" + hosts_sections[host][0]: # "/home.html"
                # do something
                content_type = "text/html"
                content = 'content'
                resp = create_response_by_fields(request_entries["Version"],'200','OK',date,server_name,str(len(content)),content_type,content)
                conn.send(resp.encode('utf-8'))
                conn.close()
                continue
            else:
                resp = version+' 404 NOT FOUND'
                # resp = bytes(resp, 'utf-8')  Eventually, another way to encode a string
                conn.send(resp.encode('utf-8'))
                conn.close()
                continue
            
        elif request_entries["Method"] == "PUT":
            print("PUT request")

        elif request_entries["Method"] == "DELETE":
            # do something
            print("DELETE request")

        elif request_entries["Method"] == "NTW22INFO":
            print("NTW22INFO request")
            
            content = get_content_by_name(host, hosts_sections)
            content_type = "text/plain"
            
            resp = create_response_by_fields(version,'200','OK',date,server_name,str(len(content)),content_type,content)

            print(resp)
            resp = bytes(resp, 'utf-8')
            conn.send(resp)

        else:
            print("Unknown request")
            conn.send(not_found_response)
            # 


    
# conn.close() HTTP/1.1 ??
s.close()