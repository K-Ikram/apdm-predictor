# -*- coding: utf-8 -*-
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient

class MongoConnection(object):

    def __init__(self):
        client = MongoClient('localhost', 8080)
        self.db = client['apdm']

    def get_collection(self, name):
        self.collection = self.db[name]
        
class TrainingSetCollection(MongoConnection):
    
    def __init__(self):
       super(TrainingSetCollection, self).__init__()
       self.get_collection('dataset')
        
    def getFHBtrainingSet(self) :
        dataset = []
        cursor = self.collection.find({"disease":"fusarium of wheat"})
        for document in cursor :
            dataset.append((document["temp_duration"], document["humidity_avg"], 
                            document["rainfall_duration"], document["weight"],
                                    document["class"], document["_id"]))
        return dataset
    
    def removeTrainingSetElement(self,element_id):
        result = self.collection.delete_one({'_id': ObjectId(element_id)})
        return result

class PredictionCollection(MongoConnection):
    
    def __init__(self):
       super(PredictionCollection, self).__init__()
       self.get_collection('prediction')


    def addFHBprediction(self, prediction, neighbors,CropProductionID):
                
        result = self.collection.insert_one(
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