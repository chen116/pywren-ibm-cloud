import tweepy
f = open("/root/twkeys.txt", "r")
consumer_key = f.readline()
consumer_secret = f.readline()
access_token = f.readline()
access_token_secret = f.readline()
print(consumer_key,consumer_secret,access_token,access_token_secret)