# -*- coding: utf-8 -*-
from DBConnection import DBConnection
from AbstractLearningDataAccess import AbstractLearningDataAccess
import datetime
import time
import sys
import cPickle
from scipy.spatial import kdtree
# patch module-level attribute to enable pickle to work
kdtree.node = kdtree.KDTree.node
kdtree.leafnode = kdtree.KDTree.leafnode
kdtree.innernode = kdtree.KDTree.innernode
sys.setrecursionlimit(10000)

class LearningDataAccess(AbstractLearningDataAccess):
    learningdDataAccess = None

    @classmethod
    def getInstance(self):
        if(self.learningdDataAccess is None):
            self.learningdDataAccess=LearningDataAccess()
        return self.learningdDataAccess

    def __init__(self):
        self.training_set_collection = DBConnection.get_collection('dataset')
        self.prediction_collection = DBConnection.get_collection('prediction')
        self.parameters_collection = DBConnection.get_collection('parameters')
        self.kdtree_collection = DBConnection.get_collection('kdtree')

    def __exit__(self, exc_type, exc_val, exc_tb):
        DBConnection.close()

######################################
#  ACCESS TO TRAINING SET COLLECTION
######################################

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

    def getTrainingSet(self,disease_name) :
        training_set = []
        cursor = self.training_set_collection.find({"disease":disease_name}).limit(100)
        for document in cursor :
            training_set.append((document["features"], document["weight"],
                                    document["class"], document["_id"]))
        return training_set

    def addTrainingSetElement(self,prediction):
        result = self.training_set_collection.insert_one(
            {   "disease":prediction["disease"],
                "features":prediction["features"],
                "class":prediction["class"],
                "weight":1
                })
        print result
        return result

######################################
#  ACCESS TO PREDICTION COLLECTION
######################################

    def addPrediction(self, prediction, CropProductionID, disease_name):
        vector = prediction[0:-2]
        result = self.prediction_collection.insert_one(
            {"prediction_date":datetime.datetime.now().replace(second=0,microsecond=0),
                "disease":disease_name,
                "crop_production":int(CropProductionID),
                "features":vector,
                "class":prediction[-2],
                "treated":False,
                "risk_rate":float(prediction[-1]),
                })

        return result

    def getPrediction(self,predictionDate, diseaseName,cropProductionID):
        dt = datetime.strptime(predictionDate,'%Y-%m-%dT%H:%M:%SZ')
        predictions = self.prediction_collection.find({"crop_production":cropProductionID,"disease":diseaseName}).sort("prediction_date",-1)
        for doc in predictions:
            d =datetime.strptime(doc["prediction_date"],'%Y-%m-%d %H:%M:%S')
            dt2 = datetime(d.year,d.month,d.day,d.hour,d.minute)
            if(dt>=dt2):
                dictionary = {
                '_id': doc['_id'],
                'disease':doc['disease'],
                'class':doc['class'],
                'risk_rate':doc['risk_rate'],
                'prediction_date':doc['prediction_date'],
                'features':doc['features']}
                return dictionary

        return None

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

######################################
#  ACCESS TO PARAMETERS COLLECTION
######################################

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

######################################
#  ACCESS TO KD TREE COLLECTION
######################################

    def getKDTree(self,disease_name):
        doc = self.kdtree_collection.find_one()
        if(doc is not None):
            # deserialize the mongodb object
            tree = cPickle.loads(str(doc["kdtree"]))
            print "KDTree restored from database"
            return tree

    def saveKDTree(self,disease_name, tree):
        raw = cPickle.dumps(tree)
        result = self.kdtree_collection.insert_one({"disease":disease_name, "kdtree":raw})
        return result
