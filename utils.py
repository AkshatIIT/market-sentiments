import re
import datetime
import pytz

def preprocess_text(text):
  text = re.sub("RT", "", text)
  text = re.sub("@[A-Za-z0-9]+", "", text) #remove mentions
  text = re.sub(r'http\S+', '', text)
  text = re.sub("#", "", text) #remove hashes
  emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", re.UNICODE)
  text = re.sub(emoj, "", text)
  text = re.sub(r"[^a-zA-Z0-9]"," ",text)
  text = text.lower()
  text = text.strip()

  return text

def get_dates(start, end, past_n_days):
      #getting start date
      start_date = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
      start_date = (start_date.replace(hour=start[0], minute=start[1], second=0, microsecond=0) - datetime.timedelta(days=past_n_days))
      print("start date: ", start_date)

      #getting end date
      end_date = (datetime.datetime.now(pytz.timezone('Asia/Kolkata')).replace(hour=end[0], minute=end[1], second=0, microsecond=0) - datetime.timedelta(days=past_n_days, seconds=10))
      print("end date: ", end_date)

      return start_date, end_date

def runner(tweets, sentiments, db, end, PAST_N_DAYS):
    #Get Dates
    start_date, end_date = get_dates((end.hour-1, end.minute), (end.hour, end.minute), PAST_N_DAYS)

    # Get processed tweets
    df = tweets.get_tweets(start_date, end_date)
    df = tweets.preprocess(df)

    # Get Sentiments
    results = sentiments.get_results(df, start_date)

    # Post data to database
    db.post_one(results)
