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
    PredictorDB = 'predictorDB'
    SystemDB = 'smartfarm'

        
    def connect(self,database):
        myConnection = MySQLdb.connect( host=self.hostname, user=self.username,
                                       passwd=self.password, db=database )        
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
        conn = self.connect(self.SystemDB)
        
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
        conn = self.connect(self.SystemDB)
        query = "select sensor.sensor_id from crop_sensor, sensor where crop_sensor.sensor_id = sensor.sensor_id and crop_sensor.crop_production_id = %s and sensor.sensor_type = %s"
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
        conn = self.connect(self.PredictorDB);
        cur = conn.cursor()
        cur.execute("SELECT TrainingSetID, TempDuration, HumidityAvg, RainfallDuration, Weight, Class FROM FHBtrainingSet" )
        
        for TrainingSetID, TempDuration, HumidityAvg, RainfallDuration, Weight, Class in cur.fetchall() :
            dataset.append((TempDuration, HumidityAvg, RainfallDuration, 
                            Weight,Class, TrainingSetID))
        
        conn.close();
        return dataset
    
    def addFHBprediction(self,prediction, neighbors,CropProductionID):
        conn = self.connect(self.PredictorDB);
        cursor=conn.cursor()
        query = """ INSERT INTO fhbpredictions(PredictionDate,CropProductionID, TempDuration,HumidityAvg, RainfallDuration, class,RiskRate)  VALUES (CURDATE(),%s,%s,%s,%s,%s,%s)"""
        cursor.execute( query, (int(CropProductionID), float(prediction[0]),float( prediction[1]),
                                float( prediction[2]), prediction[3],prediction[4]))
        last_id = cursor.lastrowid

        for x in range (len(neighbors)):
            if (neighbors[x][-2] == prediction[3]):
                sql1 = """ INSERT INTO fhbvoisinage( PredictionID, TrainingSetID) VALUES (%s,%s)"""
                cursor.execute(sql1,(float(last_id), float(neighbors[x][-1])))
        
        conn.commit()
        conn.rollback()
        conn.close()

    #Cette fonction retourne la prédiction qui concerne une culture à une date donnée
    def getFHBprediction(self,cropProductionID, predictionDate):
        conn = self.connect(self.PredictorDB)
        cur = conn.cursor()
        query= "SELECT PredictionID FROM FHBpredictions where cropProductionID = %s AND PredictionDate = %s"
        cur.execute(query,(cropProductionID,predictionDate))
        prediction =int(cur.fetchone()[0])
        conn.close()
        return prediction

    # Cette fonction retourne la liste des identifiants des voisins de 
    # la meme classes que la préidction
    def getFHBpredictionNeighbours(self,predictionId):
        neighbors=[]
        conn = self.connect(self.PredictorDB)
        cur = conn.cursor()
        query= "SELECT PredictionID, TrainingSetID FROM FHBvoisinage where PredictionID = %s"

        cur.execute(query,(predictionId,))
        for PredictionID, TrainingSetID in cur.fetchall() :
                neighbors.append(TrainingSetID)
        
        conn.close()
        return neighbors
        
    def getFHBPredictionByID(self,prediction_id):
        conn = self.connect(self.PredictorDB);
        cur=conn.cursor()
        query= "SELECT * FROM fhbpredictions where PredictionID = %s"
        cur.execute(query,(prediction_id,))
        prediction = cur.fetchone()
        
        conn.close()
        return prediction
        
# Cette fonction ajoute la prédiction correcte à l'ensemble d'apprentissage     
    def addToFHBTrainingSet(self,prediction_id):
         conn = self.connect(self.PredictorDB);
         cursor=conn.cursor()
         prediction = self.getFHBPredictionByID(prediction_id)
         query = """ INSERT INTO fhbtrainingset(TempDuration,HumidityAvg, RainfallDuration,weight, class)  VALUES (%s,%s,%s,1,%s)"""
         cursor.execute( query, (float(prediction[3]),float( prediction[4]),float( prediction[5]), prediction[6]))
         conn.close()