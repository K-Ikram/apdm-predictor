from datetime import datetime
from bson import ObjectId
# -*- coding: utf-8 -*-

from  __init__ import *


def getFHBtrainingSet() :
    dataset = []
    cursor = db.dataset.find({"disease":"fusarium of wheat"})
    for document in cursor :
        dataset.append((document["temp_duration"], document["humidity_avg"], 
                        document["rainfall_duration"], document["weight"],
                                document["class"], document["_id"]))
    
    return dataset

def addFHBprediction(prediction, neighbors,CropProductionID):
            
    result = db.prediction.insert_one(
        {"prediction_date":datetime.now().replace(hour=0,minute=0,second=0,microsecond=0),
            "disease":"fusarium of wheat",
            "crop_production":int(CropProductionID), 
            "temp_duration":int(prediction[0]),
            "humidity_avg":float(prediction[1]), 
            "rainfall_duration":int(prediction[2]), 
            "class":prediction[3], 
            "risk_rate":float(prediction[4]),
            "neighbors":neighbors
            })
    return result
    
def removeTrainingSetElement(element_id):
    result = db.dataset.delete_one({'_id': ObjectId(element_id)})
    return result