'''
Created on Feb 28, 2019

py2: ConfigParser & py3: configparser

@author: mayijie
'''

import sys, os
import configparser

class configFile:
    
    defaultCF = 'config.cfg'
    
    def __init__(self, location):
        if location == None:
            self.config = self.defaultCF
        else:
            self.config = location
        self.sectionDict = {}
        
    def loadConfig(self):

        try:
            if self.config == None:
                exc = IOError("Empty file or directory name")
                exc.errno = 2
                raise exc
            if '/' not in self.config:
                self.config = os.path.join(sys.path[0], self.config)
            config = configparser.RawConfigParser()
            config.readfp(open(self.config))
            
            sections = config.sections()
            for section in sections:
                itemDict = dict()
                items = config.items(section)
                for key, value in items:
                    itemDict[key] = value
                self.sectionDict[section] = itemDict
    
        except (IOError, Exception) as exc:
            print (exc)
            raise exc
