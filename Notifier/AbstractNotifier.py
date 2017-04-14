# -*- coding: utf-8 -*-
from DataAccess.MySQL.RessourceDataAccess import RessourceDataAccess

class AbstractNotifier():
    def __init__(self):
        self.data_access = RessourceDataAccess.getInstance()
    
    def notify(self):
        raise NotImplementedError("Send Alert is not implemented here")