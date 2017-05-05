# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 15:12:41 2017

@author: BOUEHNNI
"""
import math
import operator
from AbstractClassifier import AbstractClassifier
from DataAccess.MongoDB.LearningDataAccess import LearningDataAccess

import sys
from scipy.spatial import KDTree
import cPickle
import numpy as np
from scipy.spatial import kdtree
# patch module-level attribute to enable pickle to work
kdtree.node = kdtree.KDTree.node
kdtree.leafnode = kdtree.KDTree.leafnode
kdtree.innernode = kdtree.KDTree.innernode
sys.setrecursionlimit(10000)

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
        print "voisins", type(neighbors)
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
        data = np.array(trainingSet)[:,0]
        data = list(data)
        tree = self.learningDataAccess.getKDTree(disease_name)
        # récupérer larbre kd associé à cet ensemble d'apprentissage
        # s'il n'est pas stocké dans la BDD ==> construire un nouvel arbre
        # puis le stocker
        if(tree is None):
            tree = KDTree(data)
            self.learningDataAccess.saveKDTree(disease_name,tree)
        else:
            print tree

        if(is_k):
            param = self.learningDataAccess.getParameter(disease_name,"k")
        else:
            param = self.learningDataAccess.getParameter(disease_name,"l")
        distances, indices=tree.query(vecteurC,k=param)
        print "neighbors: distances, indices",distances, indices,"\n"

        neighbors = []
        for indice in indices:
             neighbors.append(trainingSet[indice])
        return neighbors
