# -*- coding: utf-8 -*-

import MySQLdb

class DBConnection():
    hostname = 'mysql-esi.alwaysdata.net'
    username = 'esi'
    password = 'esi'
    database = 'esi_apdm'
    db = None
    cursor  = None
        
    @classmethod
    def getCursor(self):
        if(not self.db):
            self.db = MySQLdb.connect( host=self.hostname, user=self.username,passwd=self.password, db=self.database )
            self.cursor = self.db.cursor()
            print "Connection to MySQL server"
        return self.cursor 
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()