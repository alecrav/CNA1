#!/usr/bin/python3
#
import socket
import sys

print(len(sys.argv), sys.argv[0], sys.argv[0])
# if len(sys.argv) < 2:
#     # print('usage:',sys.argv[0],'<host> [<port> (default=1234)]')
#     exit(-1)

# host_name = sys.argv[1]
host_name = 'localhost'

if len(sys.argv) > 2:
    port_number = int(sys.argv[2])
else:
    port_number = 8084

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host_name, port_number))
data = None
request = ""
while True:
    data = sys.stdin.readline()
    if (data == "\n"):
        break
    request = request + data
# request = input('<request> ')

s.send(request.encode('utf-8'))
reply = s.recv(1024)
print('reply:', reply.decode('utf-8'))
s.close()