# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:56:18 2017

@author: BOUEHNNI
"""
import MySQLdb
from DataAccess.Data import Data
class DataAccessFHB(object):
    
    hostname = 'localhost'
    username = 'root'
    password = ''
    database = 'apdm'

    def __init__(self):
        self.db = MySQLdb.connect( host=self.hostname, user=self.username,
                                       passwd=self.password, db=self.database )
        self.cursor = self.db.cursor()
        self.data_access = Data()

    def __enter__(self):
        return DataAccessFHB()


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()
        
    def getFHBmesures(self,cropProductionID):
        # recuperer une mesure de la base de données
        mesures =[]
        temperature = []
        humidity = []
        rainfall = []
        tempSensors = self.data_access.getSensors(cropProductionID,"temperature")
        humSensors = self.data_access.getSensors(cropProductionID,"humidity")
        rainSensors = self.data_access.getSensors(cropProductionID,"rainfall")
        
        queryTemp = "(SELECT measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        queryHum = "(SELECT  measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        queryRain = "(SELECT measure.measure_value FROM measure where measure.sensor_id = %s and timestampdiff(SECOND, measure.measure_timestamp , now()) < 3600*24*7) order by measure_timestamp DESC"
        
        self.cursor.execute(queryTemp, (tempSensors[0],))
        for measure in self.cursor.fetchall() :
            temperature.append(float(measure[0]))
            
        self.cursor.execute(queryHum, (humSensors[0],))
        for measure in self.cursor.fetchall() :
            humidity.append(float(measure[0]))
            
        self.cursor.execute(queryRain, (rainSensors[0],))
        for measure in self.cursor.fetchall() :
            rainfall.append(float(measure[0]))
            
        mesures.append(temperature)
        mesures.append(humidity)
        mesures.append(rainfall)   
        return mesures