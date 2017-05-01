# -*- coding: utf-8 -*-
from DataAccess.MySQL.DataAccess import DataAccess

class AbstractNotifier():
    def __init__(self):
        self.data_access = DataAccess.getInstance()
    
    def notify(self):
        raise NotImplementedError("Send Alert is not implemented here")