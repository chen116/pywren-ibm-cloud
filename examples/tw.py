from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
f = open("/root/twkeys.txt", "r")
consumer_key = f.readline().strip()
consumer_secret = f.readline().strip()
access_token = f.readline().strip()
access_token_secret = f.readline().strip()


import time,json
import pywren_ibm_cloud as pywren
import socket,fcntl,os,errno,sys
import time
import queue
import threading



def streamprocess_threads(pw,my_func,my_reduce_function,connector,host='localhost',port=65432,window=2):
    exitFlag = 0
    cnt=0
    class myThread (threading.Thread):
        def __init__(self, threadID, name, q):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.q = q
            self.cnt = 0
        def run(self):
            print("Starting " + self.name)
            while not exitFlag:
                queueLock.acquire()
                if not workQueue.empty():
                    self.cnt+=1
                    data = self.q.get()
                    queueLock.release()
                    if data:
                        pw.map_reduce(my_func,data,my_reduce_function,reducer_wait_local=False)
                else:
                    queueLock.release()
                # if self.cnt>1:
                    # break

            print("Exiting " + self.name)
    queueLock = threading.Lock()
    workQueue = queue.Queue()
    threadList = ["Thread-1", "Thread-2"]
    threads = []
    threadID = 1
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1




    class listener(StreamListener):
        def __init__(self):
            self.cnt=0
            self.batch=[]
            self.time=0

        def on_data(self, data):
            # if self.batch==[]:
            #     self.time=time.time()
            self.batch+=[json.loads(data)['text']]
            if time.time()-self.time > 2:
                self.cnt+=1
                if self.cnt>=5:
                    exitFlag=1 
                    self.on_error(420)
                    print(pw.get_result())
                sys.exit('Limit tweets reached.')
                queueLock.acquire()
                workQueue.put(self.batch)
                queueLock.release()
                self.batch=[]
                self.time=time.time()
                print("=========================",self.cnt)





        def on_error(self, status):
            print ("Error " + str(status))
            if status == 420:
                print("Rate Limited")
                return True

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print('start tw stream')
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["car"])
    print('meow')
    exitFlag=1
    for t in threads:
        t.join()
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
                ma[i]=1    
    return ma
pw = pywren.ibm_cf_executor()
streamprocess_threads(pw,my_func,my_reduce_function,"twitterStream",host='127.0.0.1',port=65432,window=2)



####################just tweepy stream#######3

# import json



# class listener(tweepy.StreamListener):
#     def __init__(self):
#         self.cnt=0


#     def on_data(self, data):
#         self.cnt+=1
#         data=json.loads(data)
#         print(data['text'])
#         return(True)

#     def on_error(self, status):
#         print(status.text)

# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# twitterStream = Stream(auth, listener())
# twitterStream.filter(track=["car"])


# import tweepy
# f = open("/root/twkeys.txt", "r")
# consumer_key = f.readline().strip()
# consumer_secret = f.readline().strip()
# access_token = f.readline().strip()
# access_token_secret = f.readline().strip()
# print(consumer_key,consumer_secret,access_token,access_token_secret)

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# print(len(public_tweets))
# for tweet in public_tweets:
#     print(tweet.text)