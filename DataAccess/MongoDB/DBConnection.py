# -*- coding: utf-8 -*-
from pymongo import MongoClient

class DBConnection(object):
    db = None

    @classmethod
    def get_collection(self,name):
        if(not self.db):
            client = MongoClient('mongodb://esi:esi@mongodb-esi.alwaysdata.net/esi_apdm', 27017)
            self.db = client.esi_apdm
            print "Connection to MongoDB Server"
        return self.db[name]
    
    def close(self):
        if(self.db):
            self.db.close()
        print "Connection closed"
