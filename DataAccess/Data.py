# -*- coding: utf-8 -*-
import MySQLdb

class Data:
        
    hostname = 'localhost'
    username = 'root'
    password = ''
    database = 'apdm'
        
    def __init__(self):
        self.db = MySQLdb.connect( host=self.hostname, user=self.username,passwd=self.password, db=self.database )        
        self.cursor = self.db.cursor()

    def __enter__(self):
        return Data()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()
    
    def getSensors(self,cropProductionID,sensorType):
        sensors = []
        query = "select sensor.sensor_id from apdm_cropproductionsensor, sensor where apdm_cropproductionsensor.sensor_id = sensor.sensor_id and apdm_cropproductionsensor.crop_production_id = %s and sensor.sensor_type = %s"
        self.cursor.execute(query, (cropProductionID,sensorType))
        
        for sensor in self.cursor.fetchall():
            sensors.append(int(sensor[0]))
        print "sensors: ", sensors
        
        return sensors 
       
    def getCurrentCropProduction(self):
        CropProduction=[]
        query= "SELECT crop_production_id, start_date, end_date, plot FROM crop_production where CURDATE()>start_date and CURDATE()<end_date"                  
        self.cursor.execute(query)
        for crop in self.cursor.fetchall():
            CropProduction.append(crop)

        return CropProduction
    
    def getCropProductionByDisease(self,diseaseID):
        CropProduction=[]
        query= "SELECT crop_production.crop_production_id FROM crop_production, apdm_cropproductiondisease where crop_production.crop_production_id = apdm_cropproductiondisease.crop_production_id and apdm_cropproductiondisease.disease_id = %s and CURDATE()>crop_production.start_date and CURDATE()<crop_production.end_date"                  
        self.cursor.execute(query,(diseaseID,))
        for crop in self.cursor.fetchall():
            CropProduction.append(int(crop[0]))

        return CropProduction
    
    def getCropDiseases(self,cropProductionID):
        diseases=[]
        query= "SELECT disease FROM apdm_cropproductiondisease where monitor_disapdm_cropproductiondiseaseease.crop_production_id=%s"                  
        self.cursor.execute(query,(cropProductionID,))
        for disease in self.cursor.fetchall():
            diseases.append(int(disease))
        return diseases
    
    def addAlert(self,cropProductionID, diseaseID,riskRate):

        query = """ INSERT INTO alert(alert_date,crop_production_id, disease_id, risk_rate)  VALUES (CURDATE(),%s,%s,%s)"""
        self.cursor.execute( query, (int(cropProductionID), int(diseaseID), int(riskRate)))
        last_id = self.cursor.lastrowid
        
        return last_id
    
    def getCropProductionClients(self,cropProductionID):
        clients=[]
        query= "SELECT apdm_client.client_id, apdm_client.first_name, apdm_client.last_name,apdm_client.phone_sms from crop_production, plot,farm, apdm_ownfarm,apdm_client where crop_production.crop_production_id=%s and crop_production.plot_id = plot.plot_id and plot.farm_id=farm.farm_id and apdm_ownfarm.farm_id = farm.farm_id and apdm_ownfarm.client_id = apdm_client.client_id"                  
        self.cursor.execute(query,(cropProductionID,))
        for client in self.cursor.fetchall():
            clients.append(client)

        return clients
        
        
    def getDiseaseName(self,diseaseID):

        query= "SELECT disease.disease_name from disease where disease.disease_id = %s"                  
        self.cursor.execute(query,(diseaseID,))
        
        return self.cursor.fetchone()[0]