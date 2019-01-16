
import socket
import time
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("server listening")
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        # while True:
            # data = conn.recv(1024)
            # if not data:
            #     break
        for i in range(15):
            conn.sendall(str(0).encode())
            time.sleep(0.5)
    print('closing')
    s.close()
