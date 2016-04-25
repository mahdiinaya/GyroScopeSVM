import time
import os, json
import ibmiotf.application
import uuid

client = None
input_state=False   
def myCommandCallback(cmd):
    global input_state
    print cmd
    if cmd.event == "light":
        payload = json.loads(cmd.payload)
        command = payload["command"]
        print command
        if command == "on":
            print "message Received:"+command
            input_state=True
        elif command == "off":
            print "message Received:"+command
	    input_state=False
try:
    options = ibmiotf.application.ParseConfigFile("/home/pi/device.cfg")


    client = ibmiotf.application.Client(options)
    client.connect()
    client.deviceEventCallback = myCommandCallback
    client.subscribeToDeviceEvents(event="light")

    while True:
    	if input_state == False:
        	print('Button Pressed')
        	myData = {'buttonPushed' : True}
        	client.publishEvent("raspberryPi", "raspPi1", "doorStatus", "json", myData)
        	time.sleep(0.2)

except ibmiotf.ConnectionException  as e:
    print e




