# -*- coding: utf-8 -*-
import MySQLdb

    
hostname = 'localhost'
username = 'root'
password = ''
db = 'apdm'

        
def connect():
    myConnection = MySQLdb.connect( host=hostname, user=username,passwd=password, db=db )        
    return myConnection
    
def getCurrentCropProduction():
    CropProduction=[]
    conn = connect()
    query= "SELECT crop_production_id, start_date, end_date, plot FROM crop_production where CURDATE()>start_date and CURDATE()<end_date"                  
    cur = conn.cursor()
    cur.execute(query)
    for crop in cur.fetchall():
        CropProduction.append(crop)
    conn.close()
    return CropProduction

def getCropProductionByDisease(diseaseID):
    CropProduction=[]
    conn = connect()
    query= "SELECT crop_production.crop_production_id FROM crop_production, apdm_cropproductiondisease where crop_production.crop_production_id = apdm_cropproductiondisease.crop_production_id and apdm_cropproductiondisease.disease_id = %s and CURDATE()>crop_production.start_date and CURDATE()<crop_production.end_date"                  
    cur = conn.cursor()
    cur.execute(query,(diseaseID,))
    for crop in cur.fetchall():
        CropProduction.append(int(crop[0]))
    conn.close()
    return CropProduction

def getCropDiseases(cropProductionID):
    diseases=[]
    conn = connect()
    query= "SELECT disease FROM apdm_cropproductiondisease where monitor_disapdm_cropproductiondiseaseease.crop_production_id=%s"                  
    cur = conn.cursor()
    cur.execute(query,(cropProductionID,))
    for disease in cur.fetchall():
        diseases.append(int(disease))
    conn.close()
    return diseases

def addAlert(cropProductionID, diseaseID,riskRate):
    conn = connect()
    query = """ INSERT INTO alert(alert_date,crop_production_id, disease_id, risk_rate)  VALUES (CURDATE(),%s,%s,%s)"""
    cursor = conn.cursor()
    cursor.execute( query, (int(cropProductionID), int(diseaseID), int(riskRate)))
    last_id = cursor.lastrowid
    return last_id

def getCropProductionClients(cropProductionID):
    clients=[]
    conn = connect()
    query= "SELECT client.client_id, client.name, client.surname,client.phone_sms from crop_production, plot,farm, apdm_ownfarm,client where crop_production.crop_production_id=%s and crop_production.plot_id = plot.plot_id and plot.farm_id=farm.farm_id and apdm_ownfarm.farm_id = farm.farm_id and apdm_ownfarm.client_id = client.client_id"                  
    cur = conn.cursor()
    cur.execute(query,(cropProductionID,))
    for client in cur.fetchall():
        clients.append(client)
    conn.close()
    return clients
    
    
def getDiseaseName(diseaseID):
    conn = connect()
    query= "SELECT disease.disease_name from disease where disease.disease_id = %s"                  
    cur = conn.cursor()
    cur.execute(query,(diseaseID,))
    
    return cur.fetchone()[0]
    
def penalizeNeighbors(neighbors, disease_id):
# prend en entré la liste des identifiants des voisins à pénaliser
    conn = connect()
    cur = conn.cursor()
    disease_table = getDiseaseTableName(disease_id)
    query= "UPDATE " + disease_table + " set weight = pow(weight,2)/2 where TrainingSetID=%s"
    for x in range(len(neighbors)):
        cur.execute(query,(neighbors[x],))
    conn.close()
    
    print "neighbors pénalisés"
    
# après 5 récompenses successives l'instance est considérée comme validée 
# et ne sera plus rejetée de la table
def rewardNeighbors(neighbors,disease_id): 
    conn = connect()
    cur = conn.cursor()
    disease_table = getDiseaseTableName(disease_id)
    query= "UPDATE "+ disease_table+" set weight = 2- pow(weight-2,2)/2 where training_set_id=%s"
    for x in range(len(neighbors)):
        cur.execute(query,(neighbors[x],))
    conn.close()
    print "neighbors récompensés"
    
    # supprimer un element de l'ensemble d'apprentissage associé à la maladie "disease_id"
def removeTrainingSetElement(disease_id, element_id):
    conn = connect()
    cur = conn.cursor()
    disease_table = getDiseaseTableName(disease_id)
    query= "DELETE from "+ disease_table+" where training_set_id=%s"
    cur.execute(query,(element_id,))
    conn.close()
    
def getDiseaseTableName(disease_id):
    if(disease_id ==1):
        return "fhb_training_set"
        
    
def updateAlert(alert_id):
    conn = connect()
    cur = conn.cursor()
    query= "UPDATE alert set feedback_treated = 1 where alert_id =%s"
    cur.execute(query,(alert_id,))
    conn.close()
    
def getConfirmedAlerts():
    alerts=[]
    conn = connect()
    query= "SELECT alert_id, alert_date, crop_production, disease from alert where alert.alert_confirmed= 1 and alert.feedback_treated=0"                  
    cur = conn.cursor()
    cur.execute(query)
    for alert in cur.fetchall():
        alerts.append(alert)
    conn.close()
    return alerts

def getDeclinedAlerts():
    alerts=[]
    conn = connect()
    query= "SELECT alert_id, alert_date, crop_production, disease from alert where alert.alert_confirmed= 0 and alert.feedback_treated=0"                  
    cur = conn.cursor()
    cur.execute(query)
    for alert in cur.fetchall():
        alerts.append(alert)
    conn.close()
    return alerts

def getAnomalies():
    anomalies=[]
    conn = connect()
    query= "SELECT anomaly_id, occurence_date, crop_production, disease from anomaly where anomaly.treated = 0"                  
    cur = conn.cursor()
    cur.execute(query)
    for anomaly in cur.fetchall():
        anomalies.append(anomaly)
    conn.close()
    return anomalies

def updateAnomaly(anomaly_id):
    conn = connect()
    cur = conn.cursor()
    query= "UPDATE anomaly set treated = 1 where anomaly_id =%s"
    cur.execute(query,(anomaly_id,))
    conn.close()
    