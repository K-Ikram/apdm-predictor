# -*- coding: utf-8 -*-
from AbstractDataAccess import AbstractDataAccess

class DiseaseDataAccess(AbstractDataAccess):
    
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

    def getMeasures(self):
        
        raise NotImplementedError("getMeasures is not implemented here")