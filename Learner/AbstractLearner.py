# -*- coding: utf-8 -*-
from DataAccess.MongoDB.AbstractLearningDataAccess import AbstractLearningDataAccess
from DataAccess.MongoDB.FusariumHeadBlightLearningDataAccess import FusariumHeadBlightLearningDataAccess
from DataAccess.MongoDB.PotatoLateBlightLearningDataAccess import PotatoLateBlightLearningDataAccess

class AbstractLearner(object):
    def __init__(self):
        self.learning_data_access = AbstractLearningDataAccess.getInstance()
        
    def penalize(self, date_occurrence, disease_name, crop_production_id):
        raise NotImplementedError("Penalize is not implemented here")
    
    def isPenalizeAllowed(self,disease_name):
        raise NotImplementedError("Is penalize allowed is not implemented here")
    
    def isRewardAllowed(self,disease_name):
        raise NotImplementedError("Is reward allowed is not implemented here")

    def reward(self, date_occurrence, disease_name, crop_production_id):
        raise NotImplementedError("Reward is not implemented here")
    
    def updateClassifier(self):
        raise NotImplementedError("Update classifier is not implemented here")
    
    def createLearningDataAccess(self,disease_name):
        if(disease_name=="Fusariose de ble"):
            return FusariumHeadBlightLearningDataAccess()
        if(disease_name=="Mildiou de la pomme de terre"):
            return PotatoLateBlightLearningDataAccess()     
