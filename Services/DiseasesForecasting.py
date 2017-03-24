
# -*- coding: utf-8 -*-

import sys
sys.path.append('D:\PFE\Developpement\Predictor3\DataAccess')
from Services import FHBPrediction
from DataAccess import DataAccessFHB
from twilio.rest import TwilioRestClient
from Data import *

account_sid = "AC6f519fcf4071615f570f2b10fe7a4a30" # Your Account SID from www.twilio.com/console
auth_token  = "d95781c0a8c685b8ddc7568d9ba28fe8"  # Your Auth Token from www.twilio.com/console
fhbPrediction = FHBPrediction.FHBPrediction()
fhbData = DataAccessFHB.DataAccessFHB()

def launchFHBForecast():
    # retrieve current crop productions
    disease_id = 1# id de la maladie 
    cropProductions=getCropProductionByDisease(disease_id)
    print "crop productions: " , cropProductions
    
    for cropProduction in cropProductions:
        #risque est un booléan : true = présence de risque / false = absence de risque
        risk_rate = fhbPrediction.predictFHB(cropProduction)
        if(risk_rate >= 0.5):
            addAlert(cropProduction, disease_id, risk_rate)# addAlert ajoute une alerte à la BDD et renvoie son identifiant
            sendAlerts(cropProduction, disease_id, risk_rate)
        else:
            print "there is no risk"
            
def sendAlerts(cropProductionID,diseaseID, risk_rate):
    #récupèrer les clients concernés par l'alerte
    clients=getCropProductionClients(cropProductionID)
    #récupérer le nom de la maladie 
    diseaseName=getDiseaseName(diseaseID)
    msgtext= "Attention Il y a un risque de "+ `diseaseName`+" dans votre culture "+`cropProductionID`+" avec un taux de "+`risk_rate`
    
    #envoi de l'alerte à tous les clients concernés
    for client in clients:
        phone_sms = client[-1]
        twilioClient = TwilioRestClient(account_sid, auth_token)        
        twilioClient.messages.create(body=msgtext,
            to=phone_sms,     # Replace with phone_sms value
            from_="+13175762039") # Replace with your Twilio number 
        print "sms sent"
        
launchFHBForecast()
