import sys
import ibmiotf.application
from flask import Flask,redirect
from flask import render_template
from flask import request
import os, json
import time

app = Flask(__name__)
vcap = json.loads(os.getenv("VCAP_SERVICES"))
port = os.getenv('VCAP_APP_PORT', '5000')
output = ""
last_readings=""
doorStatus = "opened"

def myEventCallback(myEvent):
  global output
  global last_readings
  print("%-33s%-32s%s: %s" % (myEvent.timestamp.isoformat(), myEvent.device, myEvent.event, json.dumps(myEvent.data)))
  if myEvent.event == "IMU_Readings":
      #output = output + str(myEvent.device) + str(myEvent.event) + str(json.dumps(myEvent.data)) + "\n"
      output = output + str(myEvent.device) + str(myEvent.event) + str(json.dumps(myEvent.data)) + "\n"
      last_readings = ""
  elif myEvent.event == "Event_Stop":
      last_readings = output
      output = ""



#options = {
#    "org": "dhtaya",
#    "id": "testIMUProject",
#    "auth-method": "use-token-auth",
#    "auth-key": "a-dhtaya-afxp5o9lj2",
#    "auth-token": "fCqs@l2SGr5aLWxzbn"
#}

options = {
    "org": vcap["iotf-service"][0]["credentials"]["org"],
    "id": vcap["iotf-service"][0]["credentials"]["iotCredentialsIdentifier"],
    "auth-method": "apikey",
    "auth-key": vcap["iotf-service"][0]["credentials"]["apiKey"],
    "auth-token": vcap["iotf-service"][0]["credentials"]["apiToken"]
}

try:
  client = ibmiotf.application.Client(options)
  client.connect()
except Exception as e:
  print(str(e))
  sys.exit()

print("(Press Ctrl+C to disconnect)")
client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents()

@app.route('/')
def hello():
        return '<!doctype html>\n<html><head><title>Hello from Flask</title></head><body><h1>Simple Python App to Turn a Light on and off</h1> <br /> <br /> <form action="/door/on" method="POST"> <input type="submit" value="Turn Light On"> </form> <form action="/door/off" method="POST"> <input type="submit" value="Turn Light Off"> </form>    </body></html>'

@app.route('/buttonPress')
def output_door():
    global output
    global last_readings
    return "IMU Readings:\n" + str(output) + str(last_readings)

@app.route('/door/<command>', methods=['GET','POST'])
def door_route(command):
    global doorStatus
    myData = {'DoorStatus' : doorStatus}
    client.publishCommand("LaptopRavi","rpsingh3_1", "doorState", "json", myData)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))

#while True:
#  time.sleep(1)
