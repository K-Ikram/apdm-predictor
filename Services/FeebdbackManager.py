# -*- coding: utf-8 -*-
from DataAccess.DataAccessFHB import DataAccessFHB
from DataAccess.DataAccessMongoDB import TrainingSetCollection

class FeedbackManager():
    def __init__(self):
        self.trainingsel_col = TrainingSetCollection()
        self.data_access_fhb = DataAccessFHB()
        
    
    def treatTrueNegatives(self):
        #reward neighbors of true negatives and add true negatives to the training set
        pass
        
    def clean(self):
        # vérifier l'ensemble d'apprentissage et supprimer 
        # les éléments non pertinents ayant des poids < seuil
        # clean fhb trainingSet
        trainingSet = self.trainingsel_col.getFHBtrainingSet()
        threshold = self.getThreshold(trainingSet)
        self.cleanTrainingSet(1,trainingSet,threshold)
    
        # clean late blight trainingSet
    
    def getThreshold(self,trainingSet):
        # calculte the threshold relative to a trainingSet under which the element
        # must be deleted
        threshold = 0.25
        return threshold
        
    def cleanTrainingSet(self,disease_id, trainingSet,threshold):
    
        for i in range(len(trainingSet)):
            element_id = trainingSet[i][-1]
            weight = trainingSet[i][-3]
            print "id: ",element_id, " weight: ",weight
            if(weight<= threshold):
                self.trainingsel_col.removeTrainingSetElement(disease_id,element_id)
    