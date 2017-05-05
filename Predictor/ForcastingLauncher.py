# -*- coding: utf-8 -*-
from DataAccess.MySQL.DataAccess import DataAccess
from FusariumHeadBlightPredictor import FusariumHeadBlightPredictor
from PotatoLateBlightPredictor import PotatoLateBlightPredictor


class ForcastingLauncher:

    def createPredictor(self,disease_id):
        if(disease_id==1):
            return FusariumHeadBlightPredictor()
        if(disease_id==2):
            return PotatoLateBlightPredictor()

    def launchDiseaseForecasting(self,disease_id):
        data_access =DataAccess.getInstance()
        predictor = self.createPredictor(disease_id)
        # retrieve current crop productions
        cropProductions=data_access.getCropProductionByDisease(disease_id)
        print "crop productions: " , cropProductions
        # predict disease for each crop production
        for cropProduction in cropProductions:
            predictor.predictDisease(cropProduction)
        return "fire"