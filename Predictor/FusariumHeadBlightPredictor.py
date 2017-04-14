# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:17:21 2017

@author: BOUEHNNI
"""
import numpy as np
from Classifier.WeightedKNN import WeightedKNN
from DataAccess.MySQL.FusariumHeadBlightDataAccess import FusariumHeadBlightDataAccess
from AbstractPredictor import AbstractPredictor

class FusariumHeadBlightPredictor(AbstractPredictor):
    
    def __init__(self):
        super(FusariumHeadBlightPredictor,self).__init__()
        self.data_access=FusariumHeadBlightDataAccess()

# on prédit la fusariose pour chaque parcelle contenant le blé 
# cette fonction prend en entrée la liste des parcelles contenant le blé
    def predictDisease(self, crop_production_id):     
        
        self.measures = self.data_access.getMeasures(crop_production_id) 
        # récupérer les measures climatiques
        # c'est une matrice qui contient 3 colonnes 
        # [Moyenne de la temperature, Moyenne de l'humidité,Les précipitations]
        print "measures climatiques", self.measures
        
        vectCar = self.calculateFeatures() # calculer le vecteur caractéristique
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

        
    def calculateFeatures(self):
        # calculer le vecteur caractéristique qui correspond à la fusariose de blé
        
        periodTemp = self.calculateTempDuration() # calculer la durée de la période dans laquelle
                                                  # température entre 9 et 30°C
        aveHum = np.mean(self.measures[1])  # calculer l'humidité relative moyenne
        periodRain = self.calculateRainDuration() # calculer la durée de la période des précipitations
        
        # construire un vecteur caractéristique de 3 variables
        vectCar = [periodTemp,aveHum,periodRain]
            
        return vectCar
    
    def calculateTempDuration(self):
        duration = 0
        for x in range(len(self.measures[0])):
            if ( self.measures[0][x] > 9 and self.measures[0][x] < 30 ):
                duration+=1

        return duration
    
    def calculateRainDuration(self):

        duration = 0
        for x in range(len(self.measures[2])):
            if ( self.measures[2][x] >= 0.1 ):
                duration+=1
    
        return duration