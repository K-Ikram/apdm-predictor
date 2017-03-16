# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 11:56:18 2017

@author: BOUEHNNI
"""

import MySQLdb

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
        tempSensors = self.getSensors(cropProductionID,"temperature")
        humSensors = self.getSensors(cropProductionID,"humidity")
        rainSensors = self.getSensors(cropProductionID,"rainfall")
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
    
    
    def getSensors(self, cropProductionID,sensorType):
        sensors = []
        conn = self.connect()
        query = "select sensor.sensor_id from apdm_cropproductionsensor, sensor where apdm_cropproductionsensor.sensor_id = sensor.sensor_id and apdm_cropproductionsensor.crop_production_id = %s and sensor.sensor_type = %s"
        cur = conn.cursor()
        cur.execute(query, (cropProductionID,sensorType))
        
        for sensor in cur.fetchall():
            sensors.append(int(sensor[0]))
        print "sensors: ", sensors
        conn.close()        
        return sensors
       
    def getFHBtrainingSet(self) :
        # recuperer l'ensemble d'apprentissage de la base de données
        dataset = []
        conn = self.connect();
        cur = conn.cursor()
        cur.execute("SELECT training_set_id, temp_duration, humidity_avg, rainfall_duration, weight, class FROM fhb_training_set" )
        
        for TrainingSetID, TempDuration, HumidityAvg, RainfallDuration, Weight, Class in cur.fetchall() :
            dataset.append((TempDuration, HumidityAvg, RainfallDuration, 
                            Weight,Class, TrainingSetID))
        
        conn.close();
        return dataset
    
    def addFHBprediction(self,prediction, neighbors,CropProductionID):
        conn = self.connect();
        cursor=conn.cursor()
        query = """ INSERT INTO fhb_predictions(prediction_date,crop_production_id, temp_duration,humidity_avg, rainfall_duration, class, risk_rate)  VALUES (CURDATE(),%s,%s,%s,%s,%s,%s)"""
        cursor.execute( query, (int(CropProductionID), float(prediction[0]),float( prediction[1]), float( prediction[2]), prediction[3],prediction[4]))
        last_id = cursor.lastrowid

        for x in range (len(neighbors)):
            if (neighbors[x][-2] == prediction[3]):
                sql1 = """ INSERT INTO fhb_neighborhood( prediction_id, training_set_id) VALUES (%s,%s)"""
                cursor.execute(sql1,(float(last_id), float(neighbors[x][-1])))
        
        conn.commit()
        conn.rollback()
        conn.close()

    #Cette fonction retourne la prédiction qui concerne une culture à une date donnée
    def getFHBprediction(self,cropProductionID, predictionDate):
        conn = self.connect()
        cur = conn.cursor()
        query= "SELECT prediction_id FROM fhb_predictions where crop_production_id = %s AND prediction_date = %s"
        cur.execute(query,(cropProductionID,predictionDate))
        prediction =int(cur.fetchone()[0])
        conn.close()
        return prediction

    # Cette fonction retourne la liste des identifiants des voisins de 
    # la meme classes que la préidction
    def getFHBpredictionNeighbours(self,predictionId):
        neighbors=[]
        conn = self.connect()
        cur = conn.cursor()
        query= "SELECT prediction_id, training_set_id FROM fhb_neighborhood where prediction_id = %s"

        cur.execute(query,(predictionId,))
        for PredictionID, TrainingSetID in cur.fetchall() :
                neighbors.append(TrainingSetID)
        
        conn.close()
        return neighbors
        
    def getFHBPredictionByID(self,prediction_id):
        conn = self.connect();
        cur=conn.cursor()
        query= "SELECT * FROM fhb_predictions where prediction_id = %s"
        cur.execute(query,(prediction_id,))
        prediction = cur.fetchone()
        
        conn.close()
        return prediction
        
# Cette fonction ajoute la prédiction correcte à l'ensemble d'apprentissage     
    def addToFHBTrainingSet(self,prediction_id):
         conn = self.connect();
         cursor=conn.cursor()
         prediction = self.getFHBPredictionByID(prediction_id)
         query = """ INSERT INTO fhb_training_set(temp_duration,humidity_avg, rainfall_duration,weight, class)  VALUES (%s,%s,%s,1,%s)"""
         cursor.execute( query, (float(prediction[3]),float( prediction[4]),float( prediction[5]), prediction[6]))
         conn.close()