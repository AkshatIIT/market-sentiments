import os
from dotenv import load_dotenv
from projectclasses import Tweets, Sentiments
from mongoscript import Database
import datetime
import pytz
from utils import runner

load_dotenv()

# How many days before today
PAST_N_DAYS = 0

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
token_secret = os.getenv('TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

# make Tweets object
tweets = Tweets(consumer_key, consumer_secret, access_token, token_secret, bearer_token)
# make sentiments object
sentiments = Sentiments()

# make mongo connection
uri = os.getenv("MONGO_URI")
db = Database(uri)

# get current datetime
end = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
runner(tweets, sentiments, db, end, PAST_N_DAYS)
