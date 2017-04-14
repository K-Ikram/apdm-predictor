# -*- coding: utf-8 -*-
from DiseaseDataAccess import DiseaseDataAccess

class FusariumHeadBlightDataAccess(DiseaseDataAccess):
    
    def getMeasures(self,cropProductionID):
        # recuperer une mesure de la base de données
        mesures =[]
        temperature = []
        humidity = []
        rainfall = []
        tempSensors = self.getSensors(cropProductionID,"temperature")
        humSensors = self.getSensors(cropProductionID,"humidity")
        rainSensors = self.getSensors(cropProductionID,"rainfall")
        
        queryTemp = "(SELECT measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        queryHum = "(SELECT  measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        queryRain = "(SELECT measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        
        if(len(tempSensors)>0) :            
            self.cursor.execute(queryTemp, (tempSensors[0],))
            for measure in self.cursor.fetchall() :
                temperature.append(float(measure[0]))
        
        if(len(humSensors)>0) :                        
            self.cursor.execute(queryHum, (humSensors[0],))
            for measure in self.cursor.fetchall() :
                humidity.append(float(measure[0]))

        if(len(rainSensors)>0) :                        
            self.cursor.execute(queryRain, (rainSensors[0],))
            for measure in self.cursor.fetchall() :
                rainfall.append(float(measure[0]))
            
        mesures.append(temperature)
        mesures.append(humidity)
        mesures.append(rainfall)   
        return mesures