import os
from pymongo import MongoClient
from easypc.config import config

client = MongoClient(
    os.environ.get('MONGODB_HOST', config['mongodb']['host']),
    os.environ.get('MONGODB_PORT', config['mongodb']['port'])
)

database = os.environ.get('MONGODB_DATABASE', config['mongodb']['database'])
db = client[database]

user = os.environ.get('MONGODB_USER', config['mongodb']['user'])
pw = os.environ.get('MONGODB_PASS', config['mongodb']['pass'])

if user and pw:
    db.authenticate(user, pw)
