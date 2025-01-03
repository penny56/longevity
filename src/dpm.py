'''
Created on Jan 16, 2019

@author: mayijie
'''

import zhmcclient
from configFile import configFile
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from prsm2api import *

def Singleton(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton


@Singleton
class dpm:
    def __init__(self, cf):
        
        # get hmc information from config file
        configComm = configFile(cf)
        configComm.loadConfig()
        conSection = configComm.sectionDict['connection']
        
        self.hmc_host = conSection["hmc"]
        self.__user_id = conSection["uid"]
        self.__user_psw = conSection["psw"]
        self.cpc_name = conSection["cpc"]

        self.session = zhmcclient.Session(self.hmc_host, self.__user_id, self.__user_psw, verify_cert=False)
        self.client = zhmcclient.Client(self.session)
        self.cpc = self.client.cpcs.find_by_name(self.cpc_name)

        # hmc varible Dedicate for HMC API methods rather than zhmcclient package methods
        self.hmc = createHMCConnection(hmcHost=self.hmc_host, userID=self.__user_id, userPassword=self.__user_psw)
        
    
