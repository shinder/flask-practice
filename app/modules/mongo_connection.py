from pymongo import MongoClient

url = 'mongodb://localhost:27017'
client = None

def getDB(db_name):
    global client
    if not client:
        client = MongoClient(url)
    return (client[db_name], client)
