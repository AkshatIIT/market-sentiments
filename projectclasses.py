import tweepy
import pandas as pd
import datetime
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from utils import preprocess_text, get_dates
# from dateutil import parser

class Tweets:
    def __init__(self, consumer_key, consumer_secret, access_token, token_secret, bearer_token):
        self.client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, token_secret)
    
    def get_query(self):
        niftytop40 = "RELIANCE OR TCS OR HDFCBANK OR INFY OR HINDUNILVR OR ICICIBANK OR BHARTIARTL OR SBIN OR HDFC OR BAJFINANCE OR KOTAKBANK OR ITC OR ASIANPAINT OR HCLTECH OR WIPRO OR BAJAJFINSV OR MARUTI OR AXISBANK OR SUNPHARMA OR TITAN OR ONGC OR ULTRACEMCO OR ADANIPORTS OR NESTLEIND OR JSWSTEEL OR POWERGRID OR TATASTEEL OR TATAMOTORS OR NTPC OR HDFCLIFE OR DIVISLAB OR TECHM OR COALINDIA OR GRASIM OR HINDALCO"
        query = f"(#nse OR #bse OR #nifty OR #sensex) (BSE OR NSE OR Bull OR Bear OR Buy OR Sell OR Short OR Long OR {niftytop40}) -is:retweet"
        print("Length of query: ", len(query))
        return query

    def get_tweets(self, start_date, end_date):
        #getting start and end date
        df = pd.DataFrame({}, columns=["Tweets"])
        #getting the query
        query = self.get_query()

        # querying for tweets
        tweets = self.client.search_recent_tweets(query=query, start_time=start_date, end_time=end_date, max_results=100, expansions=["geo.place_id"], place_fields=["country"])
        # print("Tweets: \n", tweets)

        # Inserting the initial tweets in df
        for tweet in tweets.data:
            df.loc[len(df.index)] = tweet.text

        print("shape of initial tweets response: ", df.shape)

        while("next_token" in tweets.meta.keys()):
            tweets = self.client.search_recent_tweets(query=query, start_time=start_date, end_time=end_date, max_results=100, next_token=tweets.meta["next_token"])
            for tweet in tweets.data:
                df.loc[len(df.index)] = tweet.text

        print("final shape of tweets df: ", df.shape)

        return df

    def preprocess(self, df):
        #pre-process the tweets
        df["Tweets"] = df["Tweets"].apply(preprocess_text)
        #dropping duplicate tweets
        df = df.drop_duplicates(ignore_index=True)
        return df

class Sentiments:
    def __init__(self):
        self.model = BertForSequenceClassification.from_pretrained("ProsusAI/finbert", num_labels=3)
        self.tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
        self.nlp = pipeline("sentiment-analysis", self.model, tokenizer=self.tokenizer)
    
    def get_sentiments(self, df):
        res = []
        for tweet in df["Tweets"]:
            res.append(self.nlp(tweet))
        
        print(f"Got {len(res)} many sentiments")
        labels = []
        scores = []
        for r in res:
            labels.append(r[0]["label"])
            scores.append(r[0]["score"])
        df["Labels"] = labels
        df["Scores"] = scores

        return df

    def get_results(self, df, start):
        df = self.get_sentiments(df)
        pos = df[df["Labels"] == "positive"].shape[0]
        neg = df[df["Labels"] == "negative"].shape[0]
        neu = df[df["Labels"] == "neutral"].shape[0]
        print(f" Positives: {pos}\n Negatives: {neg}\n", "Bullish: ", pos/(pos+neg), "\n", "Bearish: ", neg/(pos+neg))
        return {"startTime": start, "bullish": pos/(pos+neg), "totalTweets": pos+neg, "positives": pos}

