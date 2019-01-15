import socket
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    i=1
    with conn:
        print('Connected by', addr)
        while True:
            time.sleep(1)
            # data = conn.recv(1024)
            if not data:
                break
            conn.sendall(i)
            i+=1