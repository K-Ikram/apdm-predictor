# -*- coding: utf-8 -*-
from DBConnection import DBConnection

class AbstractDataAccess(object):
    
    def __init__(self):
        self.cursor = DBConnection.getCursor()
    
    
   
   