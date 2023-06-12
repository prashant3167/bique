from pymongo import MongoClient

# from utils.utils import timeit
import urllib
import toml
from datetime import datetime,timezone

config = toml.load("config.toml")


class Database:
    def __init__(self, db="bique") -> None:
        self.host = config["Mongo"]["host"]
        self.username = config["Mongo"]["user"]
        self.password = config["Mongo"]["passsword"]
        self.db = db
        self.connect()

    def connect(self):
        self.connect = MongoClient(
            f"mongodb://{self.username}:{urllib.parse.quote(self.password)}@{self.host}:27017/bique?authMechanism=DEFAULT&directConnection=true"
        )
        self.bucket = self.connect[self.db]

    def insert_update(self, document, data, primary_key):
        bucket = self.bucket[document]
        x = bucket.find_one_and_update({primary_key: data[primary_key]},
                               {"$set": data},
                               upsert=True)
        print(x.inserted_id)

    def insert_many(self, document, data):
        bucket = self.bucket[document]
        bucket.insert_many(data)
        return 0

    # @timeit
    def get_user(self, id):
        try:
            return self.bucket["users"].find({"id": id})[0]
        except:
            return None
    
    def get_account(self, id):
        try:
            return [{"source": i["iban"]} for i in self.bucket["users"].find({"id": id})[0]["accounts"]]
        except:
            return None

    def get_transactions(self, accounts, page=1):
        try:
            return list(self.bucket["transactions"].find({"$or": accounts},{"_id":0,"id":1, "amount":1, "transactionInformation": 1, "date":1, "proprietaryBankTransactionCode.issuer":1}).sort([("date", -1)]).limit(10).skip(10*(page-1)))
        except:
            return None
        
    def get_overview(self, id):
        try:
            return list(self.bucket["transactions"].aggregate([
    {
        '$addFields': {
            't_date': {
                '$dateFromString': {
                    'dateString': '$valueDateTime', 
                    'format': '%Y-%m-%d %H:%M:%S'
                }
            }
        }
    }, {
        '$match': {
            'username': str(id), 
            't_date': {
                '$gte': datetime(2023, 5, 1, 0, 0, 0, tzinfo=timezone.utc), 
                '$lte': datetime(2023, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
            }
        }
    }, {
        '$group': {
            '_id': None, 
            'income': {
                '$sum': {
                    '$cond': {
                        'if': {
                            '$gt': [
                                '$amount', 0
                            ]
                        }, 
                        'then': '$amount', 
                        'else': 0
                    }
                }
            }, 
            'spend': {
                '$sum': {
                    '$cond': {
                        'if': {
                            '$lt': [
                                '$amount', 0
                            ]
                        }, 
                        'then': '$amount', 
                        'else': 0
                    }
                }
            }, 
            'totaltransaction': {
                '$sum': {
                    '$cond': {
                        'if': {
                            '$lt': [
                                '$amount', 0
                            ]
                        }, 
                        'then': 1, 
                        'else': 0
                    }
                }
            }
        }
    }
]))[0]
        except:
            return None


# a=Database()
# a.insert('tr',{'cd':"Cdmk"})
