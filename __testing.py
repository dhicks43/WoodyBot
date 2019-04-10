from pymongo import MongoClient

client = MongoClient()

db = client.woodybot_db
ff = db.users

print(ff.find_one())