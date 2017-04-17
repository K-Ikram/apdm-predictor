# -*- coding: utf-8 -*-
from DBConnection import DBConnection
import datetime
import time       

class AbstractLearningDataAccess():
    abstractLearningdDataAccess = None

    @classmethod
    def getInstance(self):
        if(self.abstractLearningdDataAccess is None):
            self.abstractLearningdDataAccess=AbstractLearningDataAccess()
        return self.abstractLearningdDataAccess
    
    def __init__(self):
        self.training_set_collection = DBConnection.get_collection('dataset')
        self.prediction_collection = DBConnection.get_collection('prediction')
        self.parameters_collection = DBConnection.get_collection('parameters')
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        DBConnection.close()
                    
    def removeUnusefulElements(self,disease_name):
        s= self.getParameter(disease_name,"s")
        
        result = self.training_set_collection.delete_many({'weight':{"$lt":s}})
        return result
    
    def updateTrainingSetElementWeight(self,element_id, new_weight):
        result = self.training_set_collection.update_one(
                {"_id": element_id},
                {"$set": {"weight":new_weight}})
        return result
    
    def getSumWeights(self,disease_name):
        return self.training_set_collection.aggregate([{
        	"$group":
        		{
        		"_id":
        			{
        				"disease":disease_name,
        				"class":"$class"
        			},
        		"sum":
        			{
        				"$sum":"$weight"
        			}
        		}
        	}])
    
    def getModelsSizes(self,disease_name):
        return self.training_set_collection.aggregate([{
    	"$group":
    		{
    		"_id":
    			{
    				"disease":disease_name,
    				"class":"$class"
    			},
    		"count":
    			{
    				"$sum":1
    			}
    		}
    	}])
    def getTrainingSetSize(self,disease_name):
        cursor = self.training_set_collection.aggregate([{
    	"$group":
    		{
    		"_id":
    			{
    				"disease":disease_name,
    			},
    		"count":
    			{
    				"$sum":1
    			}
    		}
    	}])
        _sum = cursor.next()
        if(_sum is not None): 
            return _sum["count"]
        return 0
    
    def getRiskRates(self,crop_production, disease):
        predictions = []
        cursor = self.prediction_collection.find({"crop_production":crop_production, "disease":disease}).sort("prediction_date",-1).limit(10)
        for doc in cursor:
            risk_rate = {
            "crop_production":doc["crop_production"],
            "disease":doc["disease"],
            "risk_rate":doc["risk_rate"],
            "prediction_date":datetime.datetime.strftime(doc["prediction_date"],'%Y-%m-%dT%H:%M:%SZ')
            }
                         
            predictions.append(risk_rate)
        print predictions
        return predictions

    def getLastRiskRate(self, crop_production, disease):
        cursor = self.prediction_collection.find({"crop_production":crop_production, "disease":disease}).sort("prediction_date",-1).limit(1)
        if(cursor.count()>0):
            doc = cursor.next()
            risk_rate = {
            "crop_production":doc["crop_production"],
            "disease":doc["disease"],
            "risk_rate":doc["risk_rate"],
            "prediction_date":datetime.datetime.strftime(doc["prediction_date"],'%Y-%m-%dT%H:%M:%SZ')
            }
            return risk_rate
        else:
            return None

    
    def getPrediction(self,predictionDate, diseaseName,cropProductionID):
        raise NotImplementedError("Get prediction is not implemented here")

    def getParameter(self,disease_name, parameter_name):
        return self.parameters_collection.find_one({'disease': disease_name})[parameter_name]
    
    def updateParameter(self,disease_name, parameter_name, value):
        result = self.parameters_collection.update_one(
                {"disease": disease_name},
                {"$set": {parameter_name:value}})
        return result
    
    def getDiseasesParameters(self):
        cursor= self.parameters_collection.find()
        diseases =[]
        for doc in cursor:
            diseases.append({"disease":doc["disease"],"tn_period":doc["tn_period"]})
        return diseases
    
    # par maladie
    def getNonTreatedPredictions(self, disease_name, period):
        last_date = time.time() - period*3600
        last_date  =datetime.datetime.fromtimestamp(last_date)
        print last_date
        cursor= self.prediction_collection.find(
                {
                    'disease': disease_name,
                    "class":"non",
                    "treated":False,
                    "prediction_date":{"$lte":last_date}
                })
        predictions= []
        for doc in cursor:
            predictions.append[doc]
            print doc
            
        return predictions
             
        
    def updatePredictionState(self,prediction_id):
        result = self.prediction_collection.update_one(
                {"_id": prediction_id},
                {"$set": {"treated":True}})
        return result
    
    def addPrediction(self):
        raise NotImplementedError("Add prediction is not implemented here")
    
    def getTrainingSet(self):
        raise NotImplementedError("get Training Set is not implemented here")
        
