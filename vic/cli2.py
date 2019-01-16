import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b'This is the message.  It will be repeated.'

try:

    # Send data
    while True:
        # Receive response
        data, server = sock.recvfrom(4097)
        if data:
            print('received',data)


finally:
    print('closing socket')
    sock.close()