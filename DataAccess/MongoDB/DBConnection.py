# -*- coding: utf-8 -*-
from pymongo import MongoClient

class DBConnection(object):
    db = None

    @classmethod
    def get_collection(self,name):
        if(not self.db):
            self.db = MongoClient('localhost', 8080)['apdm']
            print "Connection to MongoDB Server"
        return self.db[name]
    
    def close(self):
        if(self.db):
            self.db.close()
        print "Connection closed"
