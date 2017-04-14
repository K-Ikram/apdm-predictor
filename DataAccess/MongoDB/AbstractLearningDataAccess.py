# -*- coding: utf-8 -*-
from DBConnection import DBConnection
from bson import ObjectId

class AbstractLearningDataAccess():
    
    def __init__(self):
        self.training_set_collection = DBConnection.get_collection('dataset')
        self.prediction_collection = DBConnection.get_collection('prediction')
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        DBConnection.close()
                    
    def removeTrainingSetElement(self,element_id):
        result = self.training_set_collection.delete_one({'_id': ObjectId(element_id)})
        return result

    def getKparameter(self):
        raise NotImplementedError("get k parameter is not implemented here")

    def addPrediction(self):
        raise NotImplementedError("Add prediction is not implemented here")
    
    def getTrainingSet(self):
        raise NotImplementedError("get Training Set is not implemented here")

        