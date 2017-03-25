# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:17:21 2017

@author: BOUEHNNI
"""
import numpy as np
from Services.WeightedKNN import WeightedKNN
from DataAccess.DataAccessFHB import DataAccessFHB
from DataAccess.DataAccessMongoDB import TrainingSetCollection, PredictionCollection


class FHBPrediction(object):
    
    def __init__(self):
        self.fhb_data_access = DataAccessFHB()
        self.dataset_col = TrainingSetCollection()
        self.prediction_col = PredictionCollection()
        self.mesures = []

# on prédit la fusariose pour chaque parcelle contenant le blé 
# cette fonction prend en entrée la liste des parcelles contenant le blé
    def predictFHB(self, crop_production_id):     
        
        self.mesures = self.fhb_data_access.getFHBmesures(crop_production_id) 
        # récupérer les mesures climatiques
        # c'est une matrice qui contient 3 colonnes 
        # [Moyenne de la temperature, Moyenne de l'humidité,Les précipitations]
        print "mesures climatiques", self.mesures
                
        fhb_training_set = self.dataset_col.getFHBtrainingSet() # récupérer l'ensemble d'apprentissage
        
        vectCar = self.calculerVCfhb() # calculer le vecteur caractéristique

        classifier = WeightedKNN(50,fhb_training_set)        
        #vectCar = classifier.normalizeVect(vectCar)
        
        neighbors= classifier.kNN(vectCar) # calculer le risque de la fusariose de blé et récupérer la liste des voisins de la prédiction créée
        self.prediction_col.addFHBprediction(vectCar, neighbors,crop_production_id) # ajouter la nouvelle prédiction au trainingSet

        # vectCar: [temp_duration, humidity_avg, rainfall_duration, resultat, risque de fusariose]
        print  "vecteur caracteristique ", vectCar
        return vectCar[-1]
        
    def calculerVCfhb(self):
        # calculer le vecteur caractéristique qui correspond à la fusariose de blé
        
        periodTemp = self.calculateTempDuration() # calculer la durée de la période dans laquelle
                                                  # température entre 9 et 30°C
        aveHum = np.mean(self.mesures[1]) # calculer l'humidité relative moyenne
        periodRain = self.calculateRainDuration() # calculer la durée de la période des précipitations
        
        # construire un vecteur caractéristique de 3 variables
        vectCar = [periodTemp,aveHum,periodRain]
            
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