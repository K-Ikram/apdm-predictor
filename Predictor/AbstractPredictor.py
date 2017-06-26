# -*- coding: utf-8 -*-

from Notifier.SMSNotifier import SMSNotifier
from Notifier.EmailNotifier import EmailNotifier

class AbstractPredictor(object):
    def __init__(self):
        self.sms_notifier = SMSNotifier()
        self.email_notifier = EmailNotifier()

    def calculateFeatures(self):
        raise NotImplementedError("calculate features is not implemented here")
    
    def predictDisease(self):
        raise NotImplementedError("predict Disease is not implemented here")
    
    
