from pymongo import MongoClient
from datetime import datetime
client = MongoClient("mongodb://127.0.0.1:8080")
db = client['apdm']

#cursor = db.prediction.delete_many({"disease":"fusarium of wheat"})
#cursor = db.dataset.update_many( 
#                {"disease": "fusarium of wheat"}, 
#                {"$set": {"weight":1}})
cursor= db.prediction.find()
for doc in cursor:
    print doc["prediction_date"]