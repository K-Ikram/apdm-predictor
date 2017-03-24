# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:17:21 2017

@author: BOUEHNNI
"""
#import sys
import numpy as np
from DataAccess import DataAccessFHB
from Services import WeightedKNN
from DataAccessMongoDB import *
class FHBPrediction(object):
    def __init__(self):
        self.fhbDataAccess = DataAccessFHB.DataAccessFHB()
        self.fhbTrainingSet = getFHBtrainingSet()
        self.classifier = WeightedKNN.WeightedKNN(50,self.fhbTrainingSet)

# on prédit la fusariose pour chaque parcelle contenant le blé 
# cette fonction prend en entrée la liste des parcelles contenant le blé
    def predictFHB(self, cropProduction):     
        # getFHBmesures() retourne mesures[] d'une parcelle ordonnées par date
        # c'est une matrice qui contient 3 colonnes 
        # 1. Moyenne de la temperature
        # 2. Moyenne de l'humidité
        # 3. Les précipitations
        self.mesures = self.fhbDataAccess.getFHBmesures(cropProduction)
        print self.mesures

        vectCar = self.calculerVCfhb()
        #vectCar = self.classifier.normalizeVect(vectCar)
        print vectCar, "vecteur"

        neighbors= self.classifier.kNN(vectCar)        
        
        addFHBprediction(vectCar, neighbors,cropProduction)
        print "fhb predicted"
        print vectCar[-1]
        return vectCar[-1]
        
    def calculerVCfhb(self):
        # calculer le vecteur caractéristique qui correspond à la fusariose de blé
        
        periodTemp = self.calculateTempDuration() # calculer la durée de la période dans laquelle
                                                  # température entre 9 et 30°C
        aveHum = np.mean(self.mesures[1]) # calculer l'humidité relative moyenne
        periodRain = self.calculateRainDuration() # calculer la durée de la période des précipitations
        
        # construire un vecteur caractéristique de 3 variables
        vectCar = [periodTemp,aveHum,periodRain]
        print vectCar
            
        return vectCar
    
    def calculateTempDuration(self):
        duration = 0
        for x in range(len(self.mesures[0])):
            if ( self.mesures[0][x] > 9 and self.mesures[0][x] < 30 ):
                duration+=1

        return duration
    
    def calculateRainDuration(self):

        duration = 0
        for x in range(len(self.mesures[2])):
            if ( self.mesures[2][x] >= 0.1 ):
                duration+=1
    
        return duration