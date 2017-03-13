

import sys
sys.path.append('D:\PFE\Developpement\Predictor2\DataAccess')
import Data
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
#        if(risk_rate >= 0.5):
#            addAlert(cropProduction, disease_id, risk_rate)# addAlert ajoute une alerte à la BDD et renvoie son identifiant
#            sendAlerts(cropProduction, disease_id)
#        else:
#            print "there is no risk"
        risk_rate = 0.95
        addAlert(cropProduction, disease_id, risk_rate)
        sendAlerts(cropProduction, disease_id)
            
def sendAlerts(cropProductionID,diseaseID):
    #récupèrer les clients concernés par l'alerte
    clients=getCropProductionClients(cropProductionID)
    #récupérer le nom de la maladie 
    diseaseName=getDiseaseName(diseaseID)
    msgtext= "Attention Il y a un risque de "+ `diseaseName`+" dans votre culture "+`cropProductionID`
    
    #envoi de l'alerte à tous les clients concernés
    for client in clients:
        phone_sms = client[-1]
        twilioClient = TwilioRestClient(account_sid, auth_token)
        
        #message = 
        twilioClient.messages.create(body=msgtext,
            to=phone_sms,     # Replace with phone_sms value
            from_="+13175762039") # Replace with your Twilio number 
        print "sms sent"
        
def treatFeedbacks():
    # traitement des vrais positifs
    alerts = getConfirmedAlerts()
    for alert in alerts:
        alert_id = alert[0]
        prediction_date = alert[1]
        crop_prediction_id = alert[2]
        disease_id = alert[3]
        treatConfirmedAlert(disease_id,alert_id,crop_prediction_id, prediction_date)
    # traitement des faux positifs
    alerts = getDeclinedAlerts()
    for alert in alerts:
        alert_id = alert[0]
        prediction_date = alert[1]
        crop_prediction_id = alert[2]
        disease_id = alert[3]
        treatDeclinedAlert(disease_id,alert_id,crop_prediction_id, prediction_date)
    # traiteement des faux négatifs
    anomalies = getAnomalies()
    for anomaly in anomalies:
        anomaly_id = anomaly[0]
        occurrence_date = anomaly[1]
        crop_prediction_id = anomaly[2]
        disease_id = anomaly[3]
        treatAnomaly(disease_id,anomaly_id,crop_prediction_id, occurrence_date)
    
    # traitement des vrais négatifs
    treatTrueNegatives()
        
def treatConfirmedAlert(disease_id, alert_id,crop_prediction_id, prediction_date):
    # get predition associated to this alert
    print "confirmed alert"
   # neighbors = []
    if (disease_id == 1):
        prediction = fhbData.getFHBprediction(crop_prediction_id,prediction_date)
        fhbData.addToFHBTrainingSet(prediction)# ajouter la prédiction correcte à l'ensemble d'apprentisssage
        print "added to fhb", prediction        
        neighbors=fhbData.getFHBpredictionNeighbours(prediction)  
    
    rewardNeighbors(neighbors, disease_id) #récompenser les voisins    
    # set alert treated at true
    updateAlert(alert_id)
        
def treatDeclinedAlert(disease_id, alert_id,crop_prediction_id, occurrence_date):
    # get predition associated to this alert
    print "declined alert"
    neighbors = []
    if (disease_id == 1):
        prediction = fhbData.getFHBprediction(crop_prediction_id,occurrence_date)
        neighbors=fhbData.getFHBpredictionNeighbours(prediction)  
    
    penalizeNeighbors(neighbors, disease_id) #récompenser les voisins
    # set alert treated at true
    updateAlert(alert_id)    

def treatAnomaly():
    print "anomaly"
    neighbors = []
    if (disease_id == 1):
        prediction = fhbData.getFHBprediction(crop_prediction_id,occurrence_date)
        neighbors=fhbData.getFHBpredictionNeighbours(prediction)  
    
    penalizeNeighbors(neighbors, disease_id) #récompenser les voisins
    # set anomaly treated at true
    updateAnomaly(anomaly_id)  

def treatTrueNegatives():
    #reward neighbors and add true negatives to the training set
    pass
    
def cleanTrainingSet():
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
        
launchFHBForecast()
#treatFeedbacks()
#cleanTrainingSet(1,fhbData.getFHBtrainingSet(),0.5)