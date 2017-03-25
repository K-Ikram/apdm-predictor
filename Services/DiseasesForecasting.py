# -*- coding: utf-8 -*-

from Services.FHBPrediction import FHBPrediction
from twilio.rest import TwilioRestClient
from DataAccess.Data import Data

class DiseaseForcasting:
    
    account_sid = "AC6f519fcf4071615f570f2b10fe7a4a30" # Your Account SID from www.twilio.com/console
    auth_token  = "d95781c0a8c685b8ddc7568d9ba28fe8"  # Your Auth Token from www.twilio.com/console
    
    def __init__(self):        
        self.fhb_prediction = FHBPrediction()
        self.data_access = Data()

    def launchFHBForecast(self):
        # retrieve current crop productions
        disease_id = 1 # id de la maladie 
        cropProductions=self.data_access.getCropProductionByDisease(disease_id)
        print "crop productions: " , cropProductions
        if cropProductions is None:
            print "none"
        
        for cropProduction in cropProductions:
            # risque est un pourcentage de présence de la maladie
            risk_rate = self.fhb_prediction.predictFHB(cropProduction)
            if(risk_rate >= 0.5):
                self.data_access.addAlert(cropProduction, disease_id, risk_rate) # addAlert ajoute une alerte à la BDD
                self.sendAlerts(cropProduction, disease_id, risk_rate)
            else:
                print "there is no risk"
                
    def sendAlerts(self,cropProductionID,diseaseID, risk_rate):
        # récupèrer les clients concernés par l'alerte
        clients=self.data_access.getCropProductionClients(cropProductionID)
        # récupérer le nom de la maladie 
        diseaseName=self.data_access.getDiseaseName(diseaseID)
        msgtext= "Attention Il y a un risque de "+ `diseaseName`+" dans votre culture "+`cropProductionID`+" avec un taux de "+`risk_rate`
        
        # envoi de l'alerte à tous les clients concernés
        for client in clients:
            phone_sms = client[-1]
            twilioClient = TwilioRestClient(self.account_sid, self.auth_token)        
            twilioClient.messages.create(body=msgtext,
                to=phone_sms,     # Replace with phone_sms value
                from_="+13175762039") # Replace with your Twilio number 
            print "sms sent"
        
df= DiseaseForcasting()
df.launchFHBForecast()