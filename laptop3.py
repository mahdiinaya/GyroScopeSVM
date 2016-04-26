import time
import os, json
import ibmiotf.device
import uuid

client = None
input_state=True   

def myCommandCallback(cmd):
    global input_state
    print cmd.data
    #print "in callback "

try:
    options = ibmiotf.device.ParseConfigFile("/home/rpsingh3/device.cfg")

    client = ibmiotf.device.Client(options)
    client.connect()
    client.commandCallback = myCommandCallback
    #client.subscribeToDeviceEvents(event="doorState")
    while True:
        time.sleep(0.1)
        pass
except ibmiotf.ConnectionException as e:
    print e


