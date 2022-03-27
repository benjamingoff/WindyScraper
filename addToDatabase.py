import json
import pymongo


def addToDatabase():
    with open('output.json') as f:
        data = json.load(f)

    client = pymongo.MongoClient("mongodb://localhost:27017")
    database = client["Weather"]
    collection = database["Weather"]

    collection.insert_one(data)
    print('Added to database')
