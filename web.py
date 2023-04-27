from flask import Flask
import paho.mqtt.publish as publish
import web
 
MQTT_SERVER = "172.20.10.12"
MQTT_PATH = "data"
import time

app = Flask(__name__)

memory = []

@app.route('/')
def record():
    
    msg = input("Enter a message to be encoded in morse format to be sent to rpi: ")
    publish.single(MQTT_PATH, msg, hostname=MQTT_SERVER)
    memory.append(msg)
    return memory
