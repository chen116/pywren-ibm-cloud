
import socket,fcntl,os
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
    now = time.time()
    batch=[]
    while True:
        try:
            data = s.recv(4)
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                print('No data available')
                continue
            else:
                print(e)
                sys.exit(1)
        else:
            batch+=[data]
            if data:
                print("Received:", repr(data))
            else:
                print('meow')
                break
            if time.time()-now > 2:
                print('batch',batch)
                batch=[]
                now=time.time()
    s.close()
    print('closed')


# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 65432  # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     # s.sendall(b"Hello, world")
#     while True:
#         data = s.recv(4)
#         if data:
#             print("Received", repr(data))
#         else:
#             print('meow')
#             break
#     s.close()
#     print('closed')
