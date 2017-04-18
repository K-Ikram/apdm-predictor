# -*- coding: utf-8 -*-
import sys
from jsonrpclib.SimpleJSONRPCServer import PooledJSONRPCServer
from jsonrpclib.threadpool import ThreadPool
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


# Setup the notification and request pools
notif_pool = ThreadPool(max_threads=10, min_threads=0)
request_pool = ThreadPool(max_threads=50, min_threads=10)

# Don't forget to start them
notif_pool.start()
request_pool.start()
port_num = int(sys.argv[1])
# Setup the server
server = PooledJSONRPCServer(('localhost', port_num), thread_pool=request_pool)
server.set_notification_pool(notif_pool)

# Register methods
server.register_function(penalize)
server.register_function(reward)
server.register_function(getLastRiskRate)
server.register_function(getRiskRates)

try:
    print "Json RPC server has been launched on port: ",port_num
    server.serve_forever()
    
finally:
    # Stop the thread pools (let threads finish their current task)
    request_pool.stop()
    notif_pool.stop()
    server.set_notification_pool(None)