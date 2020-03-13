import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from datetime import datetime, timedelta
from processData import process

import random
import time
import json

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://pollution-pkdoesml.firebaseio.com'})

'''
firedb = firestore.client()
pokemon_ref = firedb.collection('pokemon')w
docs = pokemon_ref.stream()

print("\n\nFIRESTORE")
for doc in docs:
    print('{} => {}'.format(doc.id, doc.to_dict()))
'''
# now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
# pastref = db.reference('/past')
# pastref.update({
#     now: random.randrange(25, 45, 1)
# })
# print(pastref.get()):

# pastToUpdate = ['/temp', '/humidity', '/pm2.5', '/pm10', '/aqi']
# values = [random.randrange(25, 45, 1) for _ in range(5)]

# predictedToUpdate = ['/pm2.5', '/pm10']
# values = [random.randrange(25, 45, 1) for _ in range(2)]

past = None

def callback(error):
    if(error):
        print(error)
    else:
        print("WRITE SUCCESS")
        print(datetime.now())

pastLimit = 6
predictedLimit = 6
while True:
    now = datetime.now()
    now_plus_15 = now + timedelta(minutes = 15)

    now = now.strftime("%d-%m-%Y %H:%M:%S")
    now_plus_15 = now_plus_15.strftime("%d-%m-%Y %H:%M:%S")

    # Read values from the sensor
    pastToUpdate = ['/temp', '/humidity', '/pm25', '/pm10', '/aqi']
    pastValues = [random.randrange(25, 45, 1) for _ in range(5)]

    print("PAST WRITE STARTED")
    for (path, value) in zip(pastToUpdate, pastValues):
        pastref = db.reference('/past' + path)
        result = pastref.get()
        resultLength = len(list(result.items()))
        if(resultLength>=pastLimit):
            keys_to_remove = pastref.order_by_key().limit_to_first(resultLength-pastLimit+1).get()
            keys_to_remove = list(keys_to_remove.keys())
            
            updateNull = {}
            for key in keys_to_remove:
                updateNull[key] = None
            # print(updateNull)
            db.reference('/past'+path).update(updateNull)
        pastref.push().set({
            "time": now,
            "value": value
        })
    
    dataForInference = db.reference('/past').get()
    processedData = process(dataForInference)
    print("PAST WRITE SUCCESS")
    print(datetime.now())

    predictedToUpdate = ['/pm25', '/pm10', '/aqi']
    predictedValues = [random.randrange(25, 45, 1) for _ in range(3)]
    # print("PREDICTED")
    print("PREDICT WRITE STARTED")
    for (path, value) in zip(predictedToUpdate, predictedValues):
        predictref = db.reference('/predicted' + path)
        result = predictref.get()
        resultLength = len(list(result.items()))
        if(resultLength>=predictedLimit):
            keys_to_remove = predictref.order_by_key().limit_to_first(resultLength-predictedLimit+1).get()
            keys_to_remove = list(keys_to_remove.keys())
            updateNull = {}
            for key in keys_to_remove:
                updateNull[key] = None
            # print(updateNull)
            db.reference('/predicted'+path).update(updateNull)
        predictref.push().set({
            "time": now_plus_15,
            "value": value
        })
        predicted = predictref.get()
    print("\n\nPREDICTED WRITE SUCCESS")
    print(datetime.now())
    time.sleep(8)



# print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
