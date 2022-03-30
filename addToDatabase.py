import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def addToDatabase():
    with open('output.json') as f:
        data = json.load(f)

    # Try connecting using private key
    try:
        cred = credentials.Certificate('windyapidatabase-firebase-adminsdk-p6hix-03ddb8fbaf.json')
        firebase_admin.initialize_app(cred)

        db = firestore.client()

        # Throw the data into the collection from the JSON
        # TODO: Add some better error handling/validation here?

        db.collection(u'WeatherReports').document().set(data)
        print('Added to database')

    except:
        print('Cant connect to database.')
