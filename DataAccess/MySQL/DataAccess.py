# -*- coding: utf-8 -*-

from AbstractDataAccess import AbstractDataAccess
from DBConnection import DBConnection

class DataAccess(AbstractDataAccess):
    dataAccess = None
    def __init__(self):
        self.cursor = DBConnection.getCursor()

    @classmethod
    def getInstance(self):
        if(self.dataAccess is None):
            self.dataAccess=DataAccess()
        return self.dataAccess

    def getCropProductionByDisease(self,diseaseID):
        CropProduction=[]
        query= "SELECT crop_production.crop_production_id FROM crop_production, apdm_cropproductiondisease where crop_production.crop_production_id = apdm_cropproductiondisease.crop_production_id and apdm_cropproductiondisease.disease_id = %s and CURDATE()>crop_production.start_date and CURDATE()<crop_production.end_date"
        self.cursor.execute(query,(diseaseID,))
        for crop in self.cursor.fetchall():
            CropProduction.append(int(crop[0]))

        return CropProduction

    def getCropProductionOwners(self,cropProductionID):
        clients=[]
        query= "SELECT apdm_client.client_id, apdm_client.first_name, apdm_client.last_name,apdm_client.notification_email, apdm_client.notification_sms,apdm_client.email, apdm_client.phone_sms from apdm_client, crop_client where crop_client.crop_production_id=%s and crop_client.client_id = apdm_client.client_id"
        self.cursor.execute(query,(cropProductionID,))
        for client in self.cursor.fetchall():
            clients.append(client)
        return clients

    def getCropProductionName(self,crop_production_id):
        query = "SELECT crop_production.name from crop_production where crop_production.crop_production_id=%s"
        self.cursor.execute(query,(crop_production_id,))
        name = self.cursor.fetchone()[0]
        return name

    def getSensors(self,cropProductionID,sensorType):
        sensors = []
        query = "select sensor.sensor_id from apdm_cropproductionsensor, sensor where apdm_cropproductionsensor.sensor_id = sensor.sensor_id and apdm_cropproductionsensor.crop_production_id = %s and sensor.sensor_type = %s"
        self.cursor.execute(query, (cropProductionID,sensorType))

        for sensor in self.cursor.fetchall():
            sensors.append(int(sensor[0]))
        print "sensors: ", sensors

        return sensors

    def addAlert(self,cropProductionID, diseaseID,riskRate):

        query = """ INSERT INTO alert(alert_date,crop_production_id, disease_id, risk_rate)  VALUES (CURDATE(),%s,%s,%s)"""
        self.cursor.execute( query, (int(cropProductionID), int(diseaseID), int(riskRate)))
        last_id = self.cursor.lastrowid
        return last_id

    def getMeasures(self, cropProductionID, measureType, duration):
        measures =[]
        sensors = self.getSensors(cropProductionID,measureType)
        query = "(SELECT measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < %s) order by measure_timestamp DESC"
        if(len(sensors)>0) :
            self.cursor.execute(query, (sensors[0],duration*3600*24))
            for measure in self.cursor.fetchall() :
                measures.append(float(measure[0]))
        else:
            print "there are no sensors related to this crop"
        return measures
