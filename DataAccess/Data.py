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
    query= "SELECT apdm_client.client_id, apdm_client.first_name, apdm_client.last_name,apdm_client.phone_sms from crop_production, plot,farm, apdm_ownfarm,apdm_client where crop_production.crop_production_id=%s and crop_production.plot_id = plot.plot_id and plot.farm_id=farm.farm_id and apdm_ownfarm.farm_id = farm.farm_id and apdm_ownfarm.client_id = apdm_client.client_id"                  
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