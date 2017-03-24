# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:56:18 2017

@author: BOUEHNNI
"""

import MySQLdb
from Data import getSensors
class DataAccessFHB(object):
    
    hostname = 'localhost'
    username = 'root'
    password = ''
    db = 'apdm'

        
    def connect(self):
        myConnection = MySQLdb.connect( host=self.hostname, user=self.username,
                                       passwd=self.password, db=self.db )        
        return myConnection
        
    def getFHBmesures(self,cropProductionID):
        # recuperer une mesure de la base de données
        mesures =[]
        temperature = []
        humidity = []
        rainfall = []
        tempSensors = getSensors(cropProductionID,"temperature")
        humSensors = getSensors(cropProductionID,"humidity")
        rainSensors = getSensors(cropProductionID,"rainfall")
        conn = self.connect()
        
        queryTemp = "(SELECT measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        queryHum = "(SELECT  measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        queryRain = "(SELECT measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        cur = conn.cursor()
        cur.execute(queryTemp, (tempSensors[0],))
        for measure in cur.fetchall() :
            temperature.append(float(measure[0]))
            
        cur.execute(queryHum, (humSensors[0],))
        for measure in cur.fetchall() :
            humidity.append(float(measure[0]))
            
        cur.execute(queryRain, (rainSensors[0],))
        for measure in cur.fetchall() :
            rainfall.append(float(measure[0]))
            
        mesures.append(temperature)
        mesures.append(humidity)
        mesures.append(rainfall)   
        conn.close()

        return mesures
    
    
