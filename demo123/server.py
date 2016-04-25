from flask import Flask,redirect
from flask import render_template
from flask import request
import os, json
import time
import ibmiotf.application

client = None
deviceId = os.getenv("DEVICE_ID")
vcap = json.loads(os.getenv("VCAP_SERVICES"))


def myCommandCallback(cmd):
    if cmd.event == "doorStatus":
        payload = json.loads(cmd.payload)
        command = payload["command"]
        print command
        

try:
    options = {
        "org": vcap["iotf-service"][0]["credentials"]["org"],
        "id": vcap["iotf-service"][0]["credentials"]["iotCredentialsIdentifier"],
        "auth-method": "apikey",
        "auth-key": vcap["iotf-service"][0]["credentials"]["apiKey"],
        "auth-token": vcap["iotf-service"][0]["credentials"]["apiToken"]
    }
    client = ibmiotf.application.Client(options)
    client.connect()
    client.deviceEventCallback=myCommandCallback
    client.subscribeToDeviceEvents(event="doorStatus")
    


except ibmiotf.ConnectionException as e:
    print e



app = Flask(__name__)
port = os.getenv('VCAP_APP_PORT', '5000')

@app.route('/')
def hello():
	return '<!doctype html>\n<html><head><title>Hello from Flask</title></head><body><h1>Simple Python App to Turn a Light on and off</h1> <br /> <br /> <form action="/light/on" method="POST"> <input type="submit" value="Turn Light On"> </form> <form action="/light/off" method="POST"> <input type="submit" value="Turn Light Off"> </form>    </body></html>'

@app.route('/light/<command>', methods=['GET', 'POST'])
def door_route(command):
    print command
    myData = {'command' : command}
    client.publishEvent("myMac", "myMac", "light", "json", myData) #devices can only subscribe to commands and not status
    return redirect("/", code=302)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
