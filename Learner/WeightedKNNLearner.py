from AbstractLearner import AbstractLearner
from Classifier.WeightedKNN import WeightedKNN
import math
class WeightedKNNLearner(AbstractLearner):
    weightedKNNLearner = None

    @classmethod
    def getInstance(self):
        if(self.weightedKNNLearner is None):
            self.weightedKNNLearner=WeightedKNNLearner()
        return self.weightedKNNLearner

    def __init__(self):
        super(WeightedKNNLearner,self).__init__()
        self.classifier = WeightedKNN.getInstance()

    def penalize(self, date_occurrence, disease_name, crop_production_id):

        if(self.isPenalizeAllowed(disease_name)):
            prediction = self.learning_data_access.getPrediction(date_occurrence, disease_name, crop_production_id)
            if(prediction is not None):
                neighbors = self.classifier.getNeighbors(prediction["features"],disease_name,False)
                for neighbor in neighbors:
                    if(neighbor[-2]==prediction["class"]):
                        new_weight = math.pow(neighbor[-3],2)/2
                        self.learning_data_access.updateTrainingSetElementWeight(neighbor[-1], new_weight)

                self.learning_data_access.updatePredictionState(prediction["_id"])
                # supprimer les elements non partinents de l'ensemble d'apprentissage
                self.learning_data_access.removeUnusefulElements(disease_name)
                self.updateClassifier(disease_name)
        else:
            print "I cannot penalize this training set"

    def isPenalizeAllowed(self, disease_name):
        weights = self.learning_data_access.getSumWeights(disease_name)
        alpha = self.learning_data_access.getParameter(disease_name,"alpha")

        sum_weights = []
        for doc in weights:
            sum_weights.append( doc["sum"])
        average = (sum_weights[0]+sum_weights[1])*(1-alpha)/2

        if(len(sum_weights)>1):
            if((sum_weights[0] - average)<0 or (sum_weights[1] - average)<0):
                return False
        else:
            print "there is less than 2 classes"
            return False

        sizes = self.learning_data_access.getModelsSizes(disease_name)
        gamma = self.learning_data_access.getParameter(disease_name,"gamma")

        if(len(sizes)>1):
            if(sizes[0]["count"]<gamma or sizes[1]["count"]<gamma ):
                return False
        else:
            print "there is less than 2 classes"
            return False

        return True

    def isRewardAllowed(self, disease_name):
        weights = self.learning_data_access.getSumWeights(disease_name)
        alpha = self.learning_data_access.getParameter(disease_name,"alpha")

        sum_weights = []
        for doc in weights:
            sum_weights.append( doc["sum"])
        average = (sum_weights[0]+sum_weights[1])*(1+alpha)/2

        if(len(sum_weights)>1):
            if((sum_weights[0] - average)>0 or (sum_weights[1] - average)>0):
                return False
        else:
            print "there is less than 2 classes"
            return False
        return True

    def reward(self, date_occurrence, disease_name, crop_production_id):

        if(self.isRewardAllowed(disease_name)):
            prediction = self.learning_data_access.getPrediction(date_occurrence, disease_name, crop_production_id)
            if(prediction is not None):
                neighbors = self.classifier.getNeighbors(prediction["features"],disease_name,False)
                for neighbor in neighbors:
                    #print neighbor[-3], "weight"
                    if(neighbor[-2]==prediction["class"]):
                        new_weight = 2- math.pow(neighbor[-3]-2,2)/2
                        #print neighbor[-1], "_id"
                        self.learning_data_access.updateTrainingSetElementWeight(neighbor[-1], new_weight)

                self.learning_data_access.updatePredictionState(prediction["_id"])
                self.learning_data_access.addTrainingSetElement(prediction)
                self.updateClassifier(disease_name)
            else:
                "no prediction found"
        else:
            print "I cannot reward this training set"

    def updateClassifier(self,disease_name):
        r = 0.1
        TA = 0.1
        training_set_size = self.learning_data_access.getTrainingSetSize(disease_name)
        self.learning_data_access.updateParameter(disease_name,"k",r*training_set_size)
        self.learning_data_access.updateParameter(disease_name,"l",TA*training_set_size)

    def rewardTrueNegatives(self):
        diseases_param = self.learning_data_access.getDiseasesParameters()
        for d in diseases_param:
            predictions = self.learning_data_access.getNonTreatedPredictions(d["disease"],d["tn_period"])
            for prediction in predictions:
                self.reward(prediction["prediction_date"],prediction["disease"],prediction["crop_production"])
