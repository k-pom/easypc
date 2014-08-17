from pymongo import MongoClient
from easypc.config import config

client = MongoClient(config['mongodb']['host'], config['mongodb']['port'])
db = client.easypc
