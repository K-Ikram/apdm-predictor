# -*- coding: utf-8 -*-
import MySQLdb

    
hostname = 'localhost'
username = 'root'
password = ''
PredictorDB = 'predictorDB'
SystemDB = 'smartfarm'

        
def connect(database):
    myConnection = MySQLdb.connect( host=hostname, user=username,passwd=password, db=database )        
    return myConnection
    
def getCurrentCropProduction():
    CropProduction=[]
    conn = connect(SystemDB)
    query= "SELECT crop_production_id, start_date, end_date,crop_id, plot_id FROM crop_production where CURDATE()>start_date and CURDATE()<end_date"                  
    cur = conn.cursor()
    cur.execute(query)
    for crop in cur.fetchall():
        CropProduction.append(crop)
    conn.close()
    return CropProduction

def getCropProductionByDisease(diseaseID):
    CropProduction=[]
    conn = connect(SystemDB)
    query= "SELECT crop_production.crop_production_id FROM crop_production, monitor_disease where crop_production.crop_production_id = monitor_disease.crop_production_id and monitor_disease.disease_id = %s and CURDATE()>crop_production.start_date and CURDATE()<crop_production.end_date"                  
    cur = conn.cursor()
    cur.execute(query,(diseaseID,))
    for crop in cur.fetchall():
        CropProduction.append(int(crop[0]))
    conn.close()
    return CropProduction

def getCropDiseases(cropProductionID):
    diseases=[]
    conn = connect(SystemDB)
    query= "SELECT disease_id FROM monitor_disease where monitor_disease.crop_production_id=%s"                  
    cur = conn.cursor()
    cur.execute(query,(cropProductionID,))
    for disease in cur.fetchall():
        diseases.append(int(disease))
    conn.close()
    return diseases

def addAlert(cropProductionID, diseaseID):
    conn = connect(SystemDB)
    query = """ INSERT INTO alert(alert_date,crop_production_id, disease_id)  VALUES (CURDATE(),%s,%s)"""
    cursor = conn.cursor()
    cursor.execute( query, (int(cropProductionID), int(diseaseID)))
    last_id = cursor.lastrowid
    return last_id

def getCropProductionClients(cropProductionID):
    clients=[]
    conn = connect(SystemDB)
    query= "SELECT client.client_id, client.name, client.surname,client.phone_sms from crop_production, plot,farm,own_farm,client where crop_production.crop_production_id=%s and crop_production.plot_id = plot.plot_id and plot.farm_id=farm.farm_id and own_farm.farm_id = farm.farm_id and own_farm.client_id = client.client_id"                  
    cur = conn.cursor()
    cur.execute(query,(cropProductionID,))
    for client in cur.fetchall():
        clients.append(client)
    conn.close()
    return clients
    
    
def getDiseaseName(diseaseID):
    conn = connect(SystemDB)
    query= "SELECT disease.disease_name from disease where disease.disease_id = %s"                  
    cur = conn.cursor()
    cur.execute(query,(diseaseID,))
    
    return cur.fetchone()[0]
    
def penalizeNeighbors(neighbors, disease_id):
# prend en entré la liste des identifiants des voisins à pénaliser
    conn = connect(PredictorDB)
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
    conn = connect(PredictorDB)
    cur = conn.cursor()
    disease_table = getDiseaseTableName(disease_id)
    query= "UPDATE "+ disease_table+" set weight = 2- pow(weight-2,2)/2 where TrainingSetID=%s"
    for x in range(len(neighbors)):
        cur.execute(query,(neighbors[x],))
    conn.close()
    print "neighbors récompensés"
    
def getDiseaseTableName(disease_id):
    if(disease_id ==1):
        return "FHBtrainingset"
        
    
def updateAlert(alert_id):
    conn = connect(SystemDB)
    cur = conn.cursor()
    query= "UPDATE alert set feedback_treated = 1 where alert_id =%s"
    cur.execute(query,(alert_id,))
    conn.close()
    
def getConfirmedAlerts():
    alerts=[]
    conn = connect(SystemDB)
    query= "SELECT alert_id, alert_date, crop_production_id, disease_id from alert where alert.alert_confirmed= 1 and alert.feedback_treated=0"                  
    cur = conn.cursor()
    cur.execute(query)
    for alert in cur.fetchall():
        alerts.append(alert)
    conn.close()
    return alerts

def getDeclinedAlerts():
    alerts=[]
    conn = connect(SystemDB)
    query= "SELECT alert_id, alert_date, crop_production_id, disease_id from alert where alert.alert_confirmed= 0 and alert.feedback_treated=0"                  
    cur = conn.cursor()
    cur.execute(query)
    for alert in cur.fetchall():
        alerts.append(alert)
    conn.close()
    return alerts

def getAnomalies():
    anomalies=[]
    conn = connect(SystemDB)
    query= "SELECT anomaly_id, occurence_date, crop_production_id, disease_id from anomaly where anomaly.treated = 0"                  
    cur = conn.cursor()
    cur.execute(query)
    for anomaly in cur.fetchall():
        anomalies.append(anomaly)
    conn.close()
    return anomalies

def updateAnomaly(anomaly_id):
    conn = connect(SystemDB)
    cur = conn.cursor()
    query= "UPDATE anomaly set treated = 1 where anomaly_id =%s"
    cur.execute(query,(anomaly_id,))
    conn.close()
    