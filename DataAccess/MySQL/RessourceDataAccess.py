from AbstractDataAccess import AbstractDataAccess

class RessourceDataAccess(AbstractDataAccess):
    ressourceDataAccess = None
    
    @classmethod    
    def getInstance(self):
        if(self.ressourceDataAccess is None):
            self.ressourceDataAccess=RessourceDataAccess()
        return self.ressourceDataAccess
    
    def getCropProductionByDisease(self,diseaseID):
        CropProduction=[]
        query= "SELECT crop_production.crop_production_id FROM crop_production, apdm_cropproductiondisease where crop_production.crop_production_id = apdm_cropproductiondisease.crop_production_id and apdm_cropproductiondisease.disease_id = %s and CURDATE()>crop_production.start_date and CURDATE()<crop_production.end_date"                  
        self.cursor.execute(query,(diseaseID,))
        for crop in self.cursor.fetchall():
            CropProduction.append(int(crop[0]))

        return CropProduction
        
    def getCropProductionOwners(self,cropProductionID):
        clients=[]
        query= "SELECT apdm_client.client_id, apdm_client.first_name, apdm_client.last_name,apdm_client.phone_sms from crop_production, plot,farm, apdm_ownfarm,apdm_client where crop_production.crop_production_id=%s and crop_production.plot_id = plot.plot_id and plot.farm_id=farm.farm_id and apdm_ownfarm.farm_id = farm.farm_id and apdm_ownfarm.client_id = apdm_client.client_id"                  
        self.cursor.execute(query,(cropProductionID,))
        for client in self.cursor.fetchall():
            clients.append(client)
        return clients
    
    def getCropProductionName(self,crop_production_id):
        query = "SELECT crop_production.name from crop_production where crop_production.crop_production_id=%s"
        self.cursor.execute(query,(crop_production_id,))
        name = self.cursor.fetchone()
        return name