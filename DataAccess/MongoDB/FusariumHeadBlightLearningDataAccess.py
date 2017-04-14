# -*- coding: utf-8 -*-
from datetime import datetime
from AbstractLearningDataAccess import AbstractLearningDataAccess

class FusariumHeadBlightLearningDataAccess(AbstractLearningDataAccess):
    def getKparameter(self):
        return 5    

    def getTrainingSet(self) :
        training_set = []
        cursor = self.training_set_collection.find({"disease":"Fusariose de ble"})
        for document in cursor :
            training_set.append((document["temp_duration"], document["humidity_avg"],
                            document["rainfall_duration"], document["weight"],
                                    document["class"], document["_id"]))
        return training_set

    def addPrediction(self, prediction, CropProductionID):

        result = self.prediction_collection.insert_one(
            {"prediction_date":datetime.now().replace(minute=0,second=0,microsecond=0),
                "disease":"Fusariose de ble",
                "crop_production":int(CropProductionID),
                "temp_duration":int(prediction[0]),
                "humidity_avg":float(prediction[1]),
                "rainfall_duration":int(prediction[2]),
                "class":prediction[3],
                "risk_rate":float(prediction[4]),
                })

        return result