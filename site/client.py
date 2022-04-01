#!/usr/bin/python3
#
# This is a very simple CLIENT implementation for a very very simple
# request/reply protocol.
#
import socket
import sys

if len(sys.argv) < 2:
    # print('usage:',sys.argv[0],'<host> [<port> (default=1234)]')
    exit(-1)

host_name = sys.argv[1]

if len(sys.argv) > 2:
    port_number = int(sys.argv[2])
else:
    port_number = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host_name, port_number))
request = input('request> ')
s.send(request.encode('utf-8'))
reply = s.recv(1024)
# print('reply:', reply.decode('utf-8'))
s.close()

