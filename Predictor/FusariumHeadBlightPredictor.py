# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:17:21 2017

@author: BOUEHNNI
"""
import numpy as np
from Classifier.WeightedKNN import WeightedKNN
from DataAccess.MySQL.DataAccess import DataAccess
from AbstractPredictor import AbstractPredictor

class FusariumHeadBlightPredictor(AbstractPredictor):
    
    def __init__(self):
        super(FusariumHeadBlightPredictor,self).__init__()
        self.data_access=DataAccess.getInstance()

    # on prédit la fusariose pour chaque parcelle contenant le blé 
    # cette fonction prend en entrée la liste des parcelles contenant le blé
    def predictDisease(self, crop_production_id):     
        
        vectCar = self.calculateFeatures(crop_production_id) # calculer le vecteur caractéristique
        # vectCar: [temp_duration, humidity_avg, rainfall_duration, resultat, risque de fusariose]
        print  "vecteur caracteristique ", vectCar

        classifier = WeightedKNN.getInstance()  
        
        # calculer le risque de la fusariose de blé
        prediction = classifier.classify(vectCar,"Fusariose de ble", crop_production_id)
        
        risk_rate = prediction[-1]
        print "risque de fusariose =",risk_rate
        if(risk_rate>=0.5):
            self.data_access.addAlert(crop_production_id, 1, risk_rate)
            self.sms_notifier.notify(crop_production_id, "Fusariose du blé",risk_rate)

        
    def calculateFeatures(self,crop_production_id):
        # calculer le vecteur caractéristique qui correspond à la fusariose de blé
        
        periodTemp = self.calculateTempDuration(crop_production_id) # calculer la durée de la période dans laquelle
                                                  # température entre 9 et 30°C
        aveHum = self.calculateAveHum(crop_production_id)  # calculer l'humidité relative moyenne
        periodRain = self.calculateRainDuration(crop_production_id) # calculer la durée de la période des précipitations
        
        # construire un vecteur caractéristique de 3 variables
        vectCar = [periodTemp,aveHum,periodRain]
            
        return vectCar
    
    def calculateTempDuration(self,crop_production_id):
        duration = 0
        measures = self.data_access.getMeasures(crop_production_id, "temperature", 70)
        for x in range(len(measures)):
            if ( measures[x] > 9 and measures[x] < 30 ):
                duration+=1
        return duration
    
    def calculateAveHum(self, crop_production_id):
        measures = self.data_access.getMeasures(crop_production_id,"humidity",70)
        return np.mean(measures)
        
    def calculateRainDuration(self,crop_production_id):
        measures = self.data_access.getMeasures(crop_production_id,"rainfall",70)
        duration = 0
        for x in range(len(measures)):
            if ( measures[x] >= 0.1 ):
                duration+=1
        return duration