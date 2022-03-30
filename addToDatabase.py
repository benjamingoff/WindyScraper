import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def addToDatabase():
    with open('output.json') as f:
        data = json.load(f)

    cred = credentials.Certificate('windyapidatabase-firebase-adminsdk-p6hix-03ddb8fbaf.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    db.collection(u'WeatherReports').document().set(data)
    print('Added to database')
