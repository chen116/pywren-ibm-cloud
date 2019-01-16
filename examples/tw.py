import tweepy
f = open("/root/twkeys.txt", "r")
consumer_key = f.readline().strip()
consumer_secret = f.readline().strip()
access_token = f.readline().strip()
access_token_secret = f.readline().strip()
print(consumer_key,consumer_secret,access_token,access_token_secret)