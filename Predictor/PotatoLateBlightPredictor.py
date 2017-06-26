# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:17:21 2017
@author: KAROUCHE
"""

from Classifier.WeightedKNN import WeightedKNN
from DataAccess.MySQL.DataAccess import DataAccess
from AbstractPredictor import AbstractPredictor

class PotatoLateBlightPredictor(AbstractPredictor):
        def __init__(self):
            super(PotatoLateBlightPredictor,self).__init__()
            self.data_access=DataAccess.getInstance()
    
        # on predit la fusariose pour chaque parcelle contenant le ble
        # cette fonction prend en entrée la liste des parcelles contenant le ble
        def predictDisease(self, crop_production_id):
            vectCar = self.calculateFeatures(crop_production_id) # calculer le vecteur caracteristique
            # vectCar: [temp_duration, humidity_avg, rainfall_duration, resultat, risque de fusariose]
            print  "vecteur caracteristique ", vectCar
            if (vectCar is None) : 
                return None
            classifier = WeightedKNN.getInstance()
    
            # calculer le risque de la fusariose de blé
            prediction = classifier.classify(vectCar,"Mildiou de la pomme de terre", crop_production_id)
    
            risk_rate = prediction[-1]
            print "risque de mildiou =",risk_rate
            if(risk_rate>=0.5):
                self.data_access.addAlert(crop_production_id, 1, risk_rate)
                self.sms_notifier.notify(crop_production_id, "Mildiou de la pomme de terre",risk_rate)
                self.email_notifier.notify(crop_production_id, "Mildiou de la pomme de terre",risk_rate)

            return prediction
           
    
    
        def calculateFeatures(self,crop_production_id):
            
            #Cette fonction calcule le vecteur caracteristique du mildiou de la pomme de terre.
            #Il contient 14 variables ordonnees selon le tableau presente dans le 2eme modele:
            # http://ipm.ucanr.edu/DISEASE/DATABASE/potatolateblight.html
            fact1=0
            fact2=0
            fact3=0
            fact4=0
            fact5=0
            fact6=0
            fact7=0
            fact8=0
            fact9=0
            fact10=0
            fact11=0
            fact12=0
            fact13=0
            fact14= 0
            cmp1=0
            cmp2=0
            cmp3=0
            cmp4=0
            cmp5=0
            cmp6=0
            
           
            Tmeasures = self.data_access.getMeasures(crop_production_id, "temperature", 7) # unit": C
            Hmeasures = self.data_access.getMeasures(crop_production_id,"humidity",7) 
            Rmeasures = self.data_access.getMeasures(crop_production_id,"rainfall",7) # unite :mm/h
            if(len(Tmeasures) <> len(Hmeasures) or len(Hmeasures) <> len(Rmeasures)):
                return None
             
            for x in range(len(Tmeasures)):
                #print "x=",x
                if ( Tmeasures[x] >= 10 and Tmeasures[x] <= 11.9 and (Hmeasures[x]>=90 or Rmeasures[x]>0.1)):
                    cmp1+=1              
                    
                else:
                    if(cmp1>=4):
                        fact1+=cmp1
                    if(cmp1>=10):
                        fact7+=cmp1
                    cmp1=0
                    if ( Tmeasures[x] >= 14 and Tmeasures[x] <= 15.9 and (Hmeasures[x]>=90 or Rmeasures[x]>0.1)):
                        cmp2+=1
                    else:
                        if(cmp2>=4):
                            fact2+=cmp2
                        if(cmp2>=10):
                            fact8+=cmp2
                        cmp2=0
                        if ( Tmeasures[x] >= 16 and Tmeasures[x] <= 17.9 and (Hmeasures[x]>=90 or Rmeasures[x]>0.1)):
                            cmp3+=1
                        else:
                            if(cmp3>=4):
                                fact3+=cmp3
                            if(cmp2>=10):
                                fact9+=cmp3
                            cmp3=0
                            if ( Tmeasures[x] >= 18 and Tmeasures[x] <= 19.9 and (Hmeasures[x]>=90 or Rmeasures[x]>0.1)):
                                cmp4+=1
                            else:
                                if(cmp4>=4):
                                    fact4+=cmp4
                                if(cmp4>=10):
                                    fact10+=cmp4
                                cmp4=0
                                if ( Tmeasures[x] >= 20 and Tmeasures[x] <= 21.9 and (Hmeasures[x]>=90 or Rmeasures[x]>0.1)):
                                     cmp5+=1
                                else:
                                    if(cmp5>=4):
                                        fact5+=cmp5
                                    if(cmp5>=10):
                                        fact11+=cmp5
                                    cmp5=0
                                    if ( Tmeasures[x] >= 22 and Tmeasures[x] <= 23.9 and (Hmeasures[x]>=90 or Rmeasures[x]>0.1)):
                                        cmp6+=1
                                    else:
                                        if(cmp6>=4):
                                            fact6+=cmp6
                                        if(cmp6>=10):
                                            fact12+=cmp6
                                        cmp6=0
                if ( Tmeasures[x] >= 15 and Tmeasures[x] <= 19.9):
                    fact13+=1
                if ( Hmeasures[x] <70):
                    fact14+=1
              
            vectCar = [fact1,fact2,fact3,fact4,fact5,fact6,fact7,fact8,fact9,fact10,fact11,fact12,fact13,fact14]
    
            return vectCar
    
        