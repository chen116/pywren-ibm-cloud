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


from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


#consumer key, consumer secret, access token, access secret.


class listener(StreamListener):

    def on_data(self, data):
        print(data)
        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])