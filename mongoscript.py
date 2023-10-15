from pymongo import MongoClient

class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client["sentiments"]

    def getdb(self):
        return self.db

    def post_one(self, data):
        table = self.db["market_sentiments"]
        table.insert_one(data)
    
    def post_many(self, data):
        table = self.db["market_sentiments"]
        table.insert_many(data)
    

