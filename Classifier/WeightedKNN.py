# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:12:41 2017

@author: BOUEHNNI
"""
import math
import operator
from AbstractClassifier import AbstractClassifier
from DataAccess.MongoDB.LearningDataAccess import LearningDataAccess

class WeightedKNN(AbstractClassifier):
    classifier =None

    def __init__(self):
        self.learningDataAccess = LearningDataAccess.getInstance()

    @classmethod
    def getInstance(self):
        if(self.classifier is None):
            self.classifier=WeightedKNN()
        return self.classifier


    # appliquer kNN sur un vecteur caractéristique
    def classify (self, vectC, disease_name,crop_production_id):
        neighbors = []
        riskRate=0
        neighbors = self.getNeighbors(vectC,disease_name,True)
        print "voisins", neighbors
        result, riskRate = self.getResponse(neighbors,riskRate)
        vectC.append(result);
        vectC.append(riskRate);
        self.learningDataAccess.addPrediction(vectC,crop_production_id,disease_name)

        return vectC

    # trouver la classe dominante parmi la liste des voisins en entrée
    def getResponse(self, neighbors,riskRate):
        classVotes = {}
        sum_ = 0

        for x in range(len(neighbors)):
            response = neighbors[x][-2]
            if response in classVotes:
                classVotes[response] += neighbors[x][-3]

            else:
                classVotes[response] = neighbors[x][-3]
            sum_ += neighbors[x][-3]
        sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)

        # calculer la somme pour eviter le cas ou il ya pas un risque ( taux = 0.0)
        if (sortedVotes[0][1]==sum_ and sortedVotes[0][0] == "non"):
            riskRate = 0
        else :

            if(sortedVotes[0][0] == "oui"):
                riskRate=sortedVotes[0][1]/(sum_)
            else:
                riskRate=sortedVotes[1][1]/(sum_)

        return sortedVotes[0][0], riskRate

    # trouver les voisins d'une instance en entrée ( un vecteur caractéristique)
    def getNeighbors(self,vecteurC,disease_name, is_k):

        trainingSet=self.learningDataAccess.getTrainingSet(disease_name)
        if(is_k):
        	param = self.learningDataAccess.getParameter(disease_name,"k")
        else:
        	param = self.learningDataAccess.getParameter(disease_name,"l")

        distances = []
        for x in range(len(trainingSet)):
            dist = self.euclideanDistance(vecteurC, trainingSet[x][0])
            distances.append((trainingSet[x], dist))
        distances.sort(key=operator.itemgetter(1))

        neighbors = []
        for x in range(int(param)):
            neighbors.append(distances[x][0])
            
        return neighbors

    # calculer la distance euclidienne entre deux vecteurs caracteristiques
    def euclideanDistance(self,instance1, instance2):
        distance = 0
        length = len(instance1)
        for x in range(length):
            distance += pow((instance1[x] - instance2[x]), 2)
        return math.sqrt(distance)