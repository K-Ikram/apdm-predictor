from Notifier.SMSNotifier import SMSNotifier

class AbstractPredictor(object):
    def __init__(self):
        self.sms_notifier = SMSNotifier()

    def calculateFeatures(self):
        raise NotImplementedError("calculate features is not implemented here")
    
    def predictDisease(self):
        raise NotImplementedError("predict Disease is not implemented here")
    
    
