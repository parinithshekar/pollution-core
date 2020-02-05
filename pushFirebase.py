import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from datetime import datetime

import random
import time

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://pollution-pkdoesml.firebaseio.com'})

'''
firedb = firestore.client()
pokemon_ref = firedb.collection('pokemon')
docs = pokemon_ref.stream()

print("\n\nFIRESTORE")
for doc in docs:
    print('{} => {}'.format(doc.id, doc.to_dict()))
'''

print("\n\nREALTIME")
# now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
# pastref = db.reference('/past')
# pastref.update({
#     now: random.randrange(25, 45, 1)
# })
# print(pastref.get()):

while True:
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    pastref = db.reference('/past')
    pastref.update({
        now: random.randrange(25, 45, 1)
    })
    predictref = db.reference('/predicted')
    predictref.update({
        now: random.randrange(22, 47, 12)
    })
    time.sleep(15)



# print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
