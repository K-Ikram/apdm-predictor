# -*- coding: utf-8 -*-
import sys
sys.path.append('D:\PFE\Developpement\Predictor3\DataAccess')
from Data import *
from DataAccessMongoDB import *

def treatTrueNegatives():
    #reward neighbors and add true negatives to the training set
    pass
    
def clean():
    # vérifier l'ensemble d'apprentissage et supprimer 
    # les éléments non pertinents ayant des poids < seuil
    # clean fhb trainingSet
    trainingSet = getFHBtrainingSet()
    threshold = getThreshold(trainingSet)
    cleanTrainingSet(1,trainingSet,threshold)

    # clean late blight trainingSet

def getThreshold(trainingSet):
    # calculte the threshold relative to a trainingSet under which the element
    # must be deleted
    threshold = 0.25
    return threshold
    
def cleanTrainingSet(disease_id, trainingSet,threshold):

    for i in range(len(trainingSet)):
        element_id = trainingSet[i][-1]
        weight = trainingSet[i][-3]
        print "id: ",element_id, " weight: ",weight
        if(weight<= threshold):
            removeTrainingSetElement(disease_id,element_id)
    