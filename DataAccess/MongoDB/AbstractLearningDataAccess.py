# -*- coding: utf-8 -*-

class AbstractLearningDataAccess():

    def removeUnusefulElements(self,disease_name):
        raise NotImplementedError("removeUnusefulElements is not implemented here")

    def updateTrainingSetElementWeight(self,element_id, new_weight):
        raise NotImplementedError("updateTrainingSetElementWeight is not implemented here")

    def getSumWeights(self,disease_name):
        raise NotImplementedError("getSumWeights is not implemented here")

    def getModelsSizes(self,disease_name):
        raise NotImplementedError("getModelsSizes is not implemented here")

    def getTrainingSetSize(self,disease_name):
        raise NotImplementedError("getTrainingSetSize is not implemented here")

    def getRiskRates(self,crop_production, disease):
        raise NotImplementedError("getRiskRates is not implemented here")

    def getLastRiskRate(self, crop_production, disease):
        raise NotImplementedError("getLastRiskRate is not implemented here")

    def getPrediction(self,predictionDate, diseaseName,cropProductionID):
        raise NotImplementedError("getPrediction is not implemented here")

    def getParameter(self,disease_name, parameter_name):
        raise NotImplementedError("getParameter is not implemented here")

    def updateParameter(self,disease_name, parameter_name, value):
        raise NotImplementedError("updateParameter is not implemented here")

    def getDiseasesParameters(self):
        raise NotImplementedError("getDiseasesParameters is not implemented here")

    # par maladie
    def getNonTreatedPredictions(self, disease_name, period):
        raise NotImplementedError("getNonTreatedPredictions is not implemented here")

    def updatePredictionState(self,prediction_id):
        raise NotImplementedError("updatePredictionState is not implemented here")

    def addPrediction(self,prediction):
        raise NotImplementedError("AddPrediction is not implemented here")

    def getTrainingSet(self,disease_name):
        raise NotImplementedError("getTrainingSet is not implemented here")

    def addTrainingSetElement(self):
        raise NotImplementedError("addTrainingSetElement is not implemented here")
