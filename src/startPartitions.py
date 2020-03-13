'''
Created on Nov 27, 2019

Configuration include two sections in config.cfg file
-- [connection] section include the HMC and CPC information
-- [partition] section include the partition information
   -- <partition name> array include the partition name array which will be started or stopped
      this option must be indicated in the command line as a parameter 
   
e.g.
python startPartitions.py t90.cfg ubuntu

@author: mayijie
'''

import sys, time
import zhmcclient
from configFile import configFile
from dpm import dpm
from log import log

class startPartitions:
    def __init__(self, partNameList):
        
        self.dpmObj = dpm(cf)
        self.partNameList = partNameList
        self.logger = log.getlogger(configComm.sectionDict['connection']['cpc'] + '-' + self.__class__.__name__)
        # identify the wait time until the start/stop action completed, 600 = 10mins
        self.timeout = 600
        # To out put to lifecycle module
        self.timespan = dict()
        

    def run(self):

        print "startPartitions starting >>>"
        for partName in self.partNameList:
            try:
                partObj = self.dpmObj.cpc.partitions.find(name = partName)
            except Exception as e:
                self.logger.info(partName + " start failed -- couldn't find !!!")
                continue
            if str(partObj.get_property('status')) == 'stopped':
                start = int(time.time())
                try:
                    partObj.start(wait_for_completion = True, operation_timeout = self.timeout, status_timeout = self.timeout)
                except (zhmcclient.HTTPError, Exception) as e:
                    self.logger.info(partName + " start failed !!!")
                    continue
                end = int(time.time())
                self.logger.info(partName + " start successful " + str(end - start))
                self.timespan[partName] = str(end - start)

        print "startPartitions completed ..."


if __name__ == '__main__':
    if len(sys.argv) == 3:
        cf = sys.argv[1]
        partNameSection = sys.argv[2]
    else:
        print ("Please input the config file and partition name array as a parameter!\nQuitting....")
        exit(1)
    
    try:
        configComm = configFile(cf)
        configComm.loadConfig()
    except Exception:
        print "Exit the program for config file read error"
        exit(1)

    partNameList = eval(configComm.sectionDict['partition'][partNameSection])
    
    startObj = startPartitions(partNameList)
    startObj.run()