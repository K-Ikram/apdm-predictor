# -*- coding: utf-8 -*-

from Learner.WeightedKNNLearner import WeightedKNNLearner
from DataAccess.MongoDB.AbstractLearningDataAccess import AbstractLearningDataAccess

def penalize(a,b,c):
    print a,b,c
    WeightedKNNLearner.getInstance().penalize(a,b,c)
    
def reward(a,b,c):
    print a,b,c
    WeightedKNNLearner.getInstance().reward(a,b,c) 

def getLastRiskRate(crop_production, disease):
    print crop_production, disease
    last_risk = AbstractLearningDataAccess.getInstance().getLastRiskRate(crop_production, disease)
    print last_risk
    return last_risk

def getRiskRates(crop_production, disease):
    print crop_production, disease
    risk_rates = AbstractLearningDataAccess.getInstance().getRiskRates(crop_production, disease)
    print risk_rates
    return risk_rates
    
    
#server = SimpleJSONRPCServer(('localhost', 8778))
#print "Json RPC server has been launched"
#server.register_function(penalize)
#server.register_function(reward)
#server.register_function(getLastRiskRate)
#server.register_function(getRiskRates)


from jsonrpclib.SimpleJSONRPCServer import PooledJSONRPCServer
from jsonrpclib.threadpool import ThreadPool

# Setup the notification and request pools
notif_pool = ThreadPool(max_threads=10, min_threads=0)
request_pool = ThreadPool(max_threads=50, min_threads=10)

# Don't forget to start them
notif_pool.start()
request_pool.start()

# Setup the server
server = PooledJSONRPCServer(('localhost', 8750), thread_pool=request_pool)
server.set_notification_pool(notif_pool)

# Register methods
server.register_function(penalize)
server.register_function(reward)
server.register_function(getLastRiskRate)
server.register_function(getRiskRates)

try:
    print "Json RPC server has been launched"
    server.serve_forever()
    
finally:
    # Stop the thread pools (let threads finish their current task)
    request_pool.stop()
    notif_pool.stop()
    server.set_notification_pool(None)