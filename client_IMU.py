import time
import sys
import ibmiotf.application
import ibmiotf.device


deviceOptions = ibmiotf.device.ParseConfigFile("/home/pi/Desktop/ProjectDevice.cfg")
try:
  deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
  print("Caught exception connecting device: %s" % str(e))
  sys.exit()

deviceCli.connect()
for x in range (0,30):
  data = { 'hello' : 'world', 'x' : x}
  deviceCli.publishEvent("greeting", "json", data)
  time.sleep(1)

deviceCli.disconnect()

