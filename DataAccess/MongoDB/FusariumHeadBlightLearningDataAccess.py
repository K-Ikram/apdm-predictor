# -*- coding: utf-8 -*-
from datetime import datetime
from AbstractLearningDataAccess import AbstractLearningDataAccess

class FusariumHeadBlightLearningDataAccess(AbstractLearningDataAccess):  

    def getTrainingSet(self) :
        training_set = []
        cursor = self.training_set_collection.find({"disease":"Fusariose de ble"})
        for document in cursor :
            training_set.append((document["features"]["temp_duration"], document["features"]["humidity_avg"],
                            document["features"]["rainfall_duration"], document["weight"],
                                    document["class"], document["_id"]))
        return training_set

    def addPrediction(self, prediction, CropProductionID):
        result = self.prediction_collection.insert_one(
            {"prediction_date":datetime.now().replace(second=0,microsecond=0),
                "disease":"Fusariose de ble",
                "crop_production":int(CropProductionID),
                "features":
                    {"temp_duration":int(prediction[0]),
                     "humidity_avg":float(prediction[1]),
                     "rainfall_duration":int(prediction[2])
                     },
                "class":prediction[3],
                "treated":False,
                "risk_rate":float(prediction[4]),
                })

        return result
    
    def addTrainingSetElement(self,prediction):
        result = self.training_set_collection.insert_one(
            {   "disease":prediction["disease"],
                "features":
                    {"temp_duration":int(prediction["features"][0]),
                     "humidity_avg":float(prediction["features"][1]),
                     "rainfall_duration":int(prediction["features"][2])
                     },
                "class":prediction["class"],
                "weight":1
                })
        print result
        return result
    
    def getPrediction(self,predictionDate, diseaseName,cropProductionID):
        dt = datetime.strptime(predictionDate,'%Y-%m-%dT%H:%M:%SZ')
        predictions = self.prediction_collection.find({"crop_production":cropProductionID,"disease":diseaseName}).sort("prediction_date",-1)
        for doc in predictions:
            d =datetime.strptime(doc["prediction_date"],'%Y-%m-%d %H:%M:%S')
            dt2 = datetime(d.year,d.month,d.day,d.hour,d.minute)
            if(dt>=dt2):
                dictionary = {
                '_id': doc['_id'],
                'disease':doc['disease'],
                'class':doc['class'],
                'risk_rate':doc['risk_rate'],
                'prediction_date':doc['prediction_date'], 
                'features':[doc['features']['temp_duration'],doc['features']['humidity_avg'],doc['features']['rainfall_duration']]}
                return dictionary

        return None
