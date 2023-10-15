from dotenv import load_dotenv
from mongoscript import Database
import os
from utils import get_dates

load_dotenv()

uri = os.getenv("MONGO_URI")
db = Database(uri).getdb()

start_date, end_date = get_dates((9, 30), (3, 30), 0)
data = db.market_sentiments.aggregate([{"$match": {"startTime": {"$gte": start_date}}}, {"$group": {"_id": None,"positives": {"$sum": "$positives"},"totalTweets": {"$sum": "$totalTweets"}}}])
print(start_date)
for d in data:
    print("Bullish: ", d["positives"]/d["totalTweets"])