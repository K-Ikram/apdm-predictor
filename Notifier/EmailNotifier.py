# -*- coding: utf-8 -*-

import smtplib

from AbstractNotifier import AbstractNotifier
    
class EmailNotifier(AbstractNotifier):
    email_host = 'smtp.gmail.com'
    email_port = 465
    gmail_user = 'username'  
    gmail_password = 'password'
    sent_from = 'safecrop@aitech.com'  
    subject = "Notification envoyée par la plateforme APDM"
    to=[]

    def notify(self, crop_production_id,disease_name, risk_rate):
        # récupèrer les clients concernés par l'alerte
        clients=self.data_access.getCropProductionOwners(crop_production_id)
        crop_production_name = self.data_access.getCropProductionName(crop_production_id)
        # récupérer le nom de la maladie 
        body= "Attention Il y a un risque de "+ disease_name+" dans votre culture "+crop_production_name+" avec un taux de "+str(risk_rate)
        
        # envoi de l'alerte à tous les clients concernés
        for client in clients:
            if(client[-4]):
                self.to.append(client[-2])
        msg = "\r\n".join([
          """From: %s"""%self.sent_from,
          """To:%s"""%", ".join(self.to),
          """Subject:%s"""%self.subject,
          "",
          body
          ])

        try:  
            server = smtplib.SMTP_SSL(self.email_host, self.email_port)
            server.ehlo()
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.sent_from, self.to, msg)
            server.close()
        
            print 'Email sent!'
        except:  
            print 'Something went wrong...'