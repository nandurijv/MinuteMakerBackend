from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.server_api import ServerApi
from os import environ
class connection():
    def connect(self):
        try:
            client = MongoClient(environ.get("MONGOURI"),server_api=ServerApi('1'),serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
            print(client)
        except ServerSelectionTimeoutError:
            print("server is down.")
        return client["minutes-maker"]