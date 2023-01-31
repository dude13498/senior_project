import time
#import downdetector_graber
#import internettrafficreport_graber
import Isitdown_graber
import istheservicedown
import outage_report_grabber
import combiner_v2
import os

while 1==1:
    conf=open(os.path.expanduser("~/FCC/senior_project/config.txt"),"r")
    conf_data=conf.readlines()
    print (conf_data)
    refresh=conf_data[1].split(":")
    print (refresh)
    refresh=refresh[1]
    path=conf_data[0].split(":")
    print (path)
    path=path[1][:-1]
    #downdetector_graber.downdetector()
    #internettrafficreport_graber.internettrafficreport()
    Isitdown_graber.isitdown()
    istheservicedown.istheservicedown()
    outage_report_grabber.outage()
    combiner_v2.combiner(path)
    print ("\nGOING TO SLEEP\n")
    time.sleep(int(refresh))