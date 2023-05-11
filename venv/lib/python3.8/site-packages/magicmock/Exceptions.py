'''
Created on May 13, 2013

@author: mxu
'''

class IncompleteInfoError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    
class IncorrectFormatError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    
class IncorrectConfigError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    
class UnableToRetrieveDataError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
    
class UnableToFindPathToGoBackToInitialStage(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)  