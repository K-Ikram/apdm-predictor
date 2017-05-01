# -*- coding: utf-8 -*-

class AbstractDataAccess(object):

    def getSensors(self,cropProductionID,sensorType):
        raise NotImplementedError("getSensors is not implemented here")

    def getMeasures(self, cropProductionID, measureType, duration):
        raise NotImplementedError("getMeasures is not implemented here")

    def getCropProductionByDisease(self,diseaseID):
        raise NotImplementedError("getCropProductionByDisease is not implemented here")

    def getCropProductionOwners(self,cropProductionID):
        raise NotImplementedError("getCropProductionOwners is not implemented here")

    def getCropProductionName(self,crop_production_id):
        raise NotImplementedError("getCropProductionName is not implemented here")

    def addAlert(self,cropProductionID, diseaseID,riskRate):
        raise NotImplementedError("addAlert is not implemented here")
