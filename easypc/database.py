import os
from pymongo import MongoClient

client = MongoClient(
    os.environ.get('MONGODB_HOST'),
    int(os.environ.get('MONGODB_PORT'))
)

database = os.environ.get('MONGODB_DATABASE')
db = client[database]

user = os.environ.get('MONGODB_USER')
pw = os.environ.get('MONGODB_PASS')

if user and pw:
    db.authenticate(user, pw)
