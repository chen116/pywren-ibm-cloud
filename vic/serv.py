import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on port',server_address)
sock.bind(server_address)

while True:
    print('waiting to receive message')
    data, address = sock.recvfrom(4096)
    print('received bytes from', len(data), address)
    print(data)
    
    if data:
        sent = sock.sendto(data, address)
        print ('send afata bacl',sent, address)