import tweepy
f = open("/root/twkeys.txt", "r")
consumer_key = f.readline().strip()
consumer_secret = f.readline().strip()
access_token = f.readline().strip()
access_token_secret = f.readline().strip()
print(consumer_key,consumer_secret,access_token,access_token_secret)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
print(len(public_tweets))
# for tweet in public_tweets:
#     print(tweet.text)


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
    def on_data(self, data):
        print(data)
        return(True)
    def on_error(self, status):
        print(status)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())
myStream.filter(track=['python'])

