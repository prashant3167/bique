from pymongo import MongoClient

# from utils.utils import timeit
import urllib
import toml

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
            f"mongodb://{self.username}:{urllib.parse.quote(self.password)}@{self.host}:27017/"
        )
        self.bucket = self.connect[self.db]

    def insert(self, document, data):
        bucket = self.bucket[document]
        x = bucket.insert_one(data)
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


# a=Database()
# a.insert('tr',{'cd':"Cdmk"})
