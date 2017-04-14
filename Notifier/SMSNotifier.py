# -*- coding: utf-8 -*-
from AbstractNotifier import AbstractNotifier
from twilio.rest import TwilioRestClient
    
class SMSNotifier(AbstractNotifier):
    account_sid = "AC6f519fcf4071615f570f2b10fe7a4a30" # Your Account SID from www.twilio.com/console
    auth_token  = "d95781c0a8c685b8ddc7568d9ba28fe8"  # Your Auth Token from www.twilio.com/console

    def notify(self, crop_production_id,disease_name, risk_rate):
        # récupèrer les clients concernés par l'alerte
        clients=self.data_access.getCropProductionOwners(crop_production_id)
        crop_production_name = self.data_access.getCropProductionName(crop_production_id)
        # récupérer le nom de la maladie 
        msgtext= "Attention Il y a un risque de "+ `disease_name`+" dans votre culture "+`crop_production_name`+" avec un taux de "+`risk_rate`
        
        # envoi de l'alerte à tous les clients concernés
        for client in clients:
        
            phone_sms = client[-1]
            twilioClient = TwilioRestClient(self.account_sid, self.auth_token)        
            twilioClient.messages.create(body=msgtext,
                to=phone_sms,     # Replace with phone_sms value
                from_="+13175762039") # Replace with your Twilio number 
            
            print "sms sent"