"""
Simple PyWren example using one single function invocation
"""
import pywren_ibm_cloud as pywren
import socket,fcntl,os,errno
import time
import queue
import threading


def streamprocess_threads(pw,my_func,my_reduce_function,connector='socket',host='localhost',port=65432,window=2):
    
    exitFlag = 0
    class myThread (threading.Thread):
        def __init__(self, threadID, name, q):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.q = q
        def run(self):
            print("Starting " + self.name)
            while not exitFlag:
                queueLock.acquire()
                if not workQueue.empty():
                    data = self.q.get()
                    queueLock.release()
                    if data:
                        pw.map_reduce(my_func,data,my_reduce_function,reducer_wait_local=False)
                else:
                    queueLock.release()
            print("Exiting " + self.name)
    queueLock = threading.Lock()
    workQueue = queue.Queue()
    threadList = ["Thread-1", "Thread-2", "Thread-3"]
    threads = []
    threadID = 1
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        now = time.time()
        batch=[]
        while True:
            try:
                data = s.recv(4)
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
                else:
                    print(e)
                    sys.exit(1)
            else:
                if data:
                    batch+=[int(data.decode())]
                    print("Received:", repr(data))
                else:
                    print('meow')
                    exitFlag = 1
                    break
                if time.time()-now > 2:
                    print('batch',batch)
                    queueLock.acquire()
                    workQueue.put(batch)
                    queueLock.release()
                    batch=[]
                    now=time.time()
        s.close()
        print('closed')
    for t in threads:
        t.join()
    print(pw.get_result())


#================== no thread ================

def streamprocess(pw,my_func,my_reduce_function,connector='socket',host='localhost',port=65432,window=2):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        now = time.time()
        batch=[]
        while True:
            try:
                data = s.recv(4)
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
                else:
                    print(e)
                    sys.exit(1)
            else:
                if data:
                    batch+=[int(data.decode())]
                    print("Received:", repr(data))
                else:
                    print('meow')
                    break
                if time.time()-now > 2:
                    print('batch',batch)
                    pw.map_reduce(my_func,batch,my_reduce_function,reducer_wait_local=False)
                    batch=[]
                    now=time.time()
        s.close()
        print('closed')

    print(pw.get_result())





def my_func(x):
	return x.split()
def my_reduce_function(results):
    ma={}
    for x in results:
        for i in x:
            if i in ma:
                ma[i]+=1
            else:
                ma[i]=0    
    return ma
pw = pywren.ibm_cf_executor()
streamprocess_threads(pw,my_func,my_reduce_function,connector='socket',host='127.0.0.1',port=65432,window=2)





######################################################################

# def my_function(x):
#     return x + 7

# if __name__ == '__main__':
#     pw = pywren.ibm_cf_executor()
#     print(pw.executor.invoker.client.is_cf_cluster)
#     pw.call_async(my_function, 3)
#     print (pw.get_result())
