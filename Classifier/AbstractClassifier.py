# -*- coding: utf-8 -*-
from DataAccess.MongoDB.FusariumHeadBlightLearningDataAccess import FusariumHeadBlightLearningDataAccess
from DataAccess.MongoDB.PotatoLateBlightLearningDataAccess import PotatoLateBlightLearningDataAccess
class AbstractClassifier():
    
    def classify(self):
        raise NotImplementedError("Classify method is not implemented here")
        
    def createLearningDataAccess(self,disease_name):
        if(disease_name == "Fusariose de ble"):
            return FusariumHeadBlightLearningDataAccess()
        if(disease_name == "Mildiou de pomme de terre"):
            return PotatoLateBlightLearningDataAccess()
        
