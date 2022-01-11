from pymongo import MongoClient
import redis 

CONNECTION_TO_MONGODB = "mongodb+srv://Bohdan:2164@hw10.gzzpv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_TO_MONGODB)
db = client.addressbook

redis_db = redis.Redis(host = 'localhost', port = 6379, db = 0)

list_cache = list(redis_db.scan_iter())