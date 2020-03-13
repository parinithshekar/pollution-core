import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from datetime import datetime, timedelta

import random
import time
import json

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://pollution-pkdoesml.firebaseio.com'})


# d = datetime.strptime("08-02-2020 20:44:53", "%d-%m-%Y %H:%M:%S")
ref = db.reference("/")
res = json.dumps(ref.get(), indent=2)
r = db.reference("/past/aqi/").order_by_key().limit_to_first(1).get()
print(json.dumps(r, indent=2))