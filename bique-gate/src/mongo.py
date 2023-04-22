
from pymongo import MongoClient
# from utils.utils import timeit
import urllib 


# Requires the PyMongo package.
# https://api.mongodb.com/python/current

# client = MongoClient('mongodb://root:password@localhost:27017/')
# filter={}

# result = client['coupon_system']['coupons'].find(
#   filter=filter
# )


class Database:
    def __init__(self, username="bdm", password="bdm", host="10.4.41.51", db="bique") -> None:
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.connect()

    def connect(self):
      self.connect = MongoClient(f'mongodb://{self.username}:{urllib.parse.quote(self.password)}@{self.host}:27017/')
      self.bucket = self.connect[self.db]
        # self.connect = Cluster.connect(
        #     f"couchbase://{self.host}?ssl=no_verify&tcp_keepalive=true",
        #     ClusterOptions(PasswordAuthenticator(self.username, self.password)),
        # ).bucket(self.db)

    def insert(self,document, data):
      bucket =  self.bucket[document]
      x = bucket.insert_one(data)
      print(x.inserted_id)
    
    # @timeit
    def get_rule(self, rule_id):
      try:
        return self.bucket['coupon_rules'].find({"rule_id": rule_id})[0]
      except:
        return None

    # @timeit
    def get_coupon(self, coupon):
      try:
        return self.bucket['coupons'].find({"code": coupon})[0]
      except:
        return None
    
    # @timeit
    def get_customer(self, username):
      try:
        return self.bucket['customers'].find({"username": username})[0]
      except:
        return None


# a=Database()
# a.insert('tr',{'cd':"Cdmk"})