import time
import paho.mqtt.client as mqtt
import json

username = "use-token-auth"
password = "aS+a+OW!72hCyhT_)*"
organization = "388z2p"
deviceType="myMac"
id="myMac"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot-2/evt/light/fmt/json", qos=2)
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    latestMessage 
    latestMessage = str(msg.payload)
    print latestMessage


clientID = "d:" + organization + ":" + deviceType + ":" + id


client = mqtt.Client(clientID)
client.username_pw_set(username, password=password)
broker = organization + ".messaging.internetofthings.ibmcloud.com"

try:
    client.connect(host=broker, port=1883, keepalive=60)
except:
    sys.exit(0)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

while True:
    pass
