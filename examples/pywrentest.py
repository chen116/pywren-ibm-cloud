"""
Simple PyWren example using one single function invocation
"""
import pywren_ibm_cloud as pywren
import socket,fcntl,os
import time
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

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
# my_source = my_source(socket,window=5)


def my_source(pw,my_func,connector='socket',host='localhost',port='65432',window=5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        # s.sendall(b"Hello, world")
        now = time.time()
        while True:
            try:
                data = s.recv(4)
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    print('No data available')
                    continue
                else:
                    print(e)
                    sys.exit(1)
            else:
                if data:
                    print("Received", repr(data))
                else:
                    print('meow')
                break
        s.close()
        print('closed')





def my_func(x):
	return sum(x)
pw = pywren.ibm_cf_executor()
streamprocess(pw,my_func,connector='socket',host='127.0.0.1',port='65432',window=5)





######################################################################

def my_function(x):
    return x + 7

if __name__ == '__main__':
    pw = pywren.ibm_cf_executor()
    print(pw.executor.invoker.client.is_cf_cluster)
    pw.call_async(my_function, 3)
    print (pw.get_result())
