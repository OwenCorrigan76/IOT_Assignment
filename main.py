
#!/usr/bin/python3
#**************************************
from flask import Flask
import requests
import paho.mqtt.client as mqtt
import subprocess
import datetime, time
import json
from sense_hat import SenseHat
from dotenv import dotenv_values


devices = [{"name":"Jude's PS4", "mac":"A4:FC:77:FD:BD:59"}]
maxTime=30  # Maximum time allowed on device in seconds
startTime= 0 # Time device first detected on network
BLYNK_AUTH = 'vhNbxWI_0MjRarIMiY51Cd-SJj2rccgb'
config = dotenv_values(".env2")

# initialize Blynk
#blynk = BlynkLib.Blynk(BLYNK_AUTH)

#initialise SenseHAT

sense = SenseHat()
sense.clear()

green = [0, 255, 0]
purple = (109, 53, 183)

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connection Result: " + str(rc))

def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

sense = SenseHat()
sense.clear()
config = dotenv_values(".env")
interval = int("10")

mqttc = mqtt.Client(client_id=config["clientId"])


# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# connect to Broker
mqttc.username_pw_set(config["username"], config["password"])

mqttc.connect("mqtt3.thingspeak.com", 1883)
mqttc.loop_start()
topic1 = "channels/1605638/publish"
mqttc.tls_set("./broker.thingspeak.crt")

app = Flask(__name__)

outcome = 0

def publish(device, message):
    message = json.dumps({"device":device, "timestamp":time.time()})
    print("publishing presence: " + message)
    
#Publish Time Expired (just needs MQTT part!)
def publishTimeExpired(device, message):
    message = json.dumps({"device":device,"message":message, "timestamp":time.time()})
    print("Device Expired: " + message)


#find the device with required MAC address and if found, publish a result to topic1 (thingSpeak)
#send an email using IFTTT notiying that the device is online
def find_devices():
    global outcome
    output = subprocess.check_output("sudo nmap -sn 192.168.1.0/24 | grep MAC", shell=True)
    devices_found=[]
    for dev in devices:  
        if dev["mac"].lower() in str(output).lower():
                print(dev["name"] + " is currently ONLINE")
                devices_found.append(dev)
                payload="field1="+str(1)
                mqttc.publish(topic1, payload)
                publish(dev, "online" )
                outcome = 1
                requests.get('https://maker.ifttt.com/trigger/Jude/with/key/bLNgGMVBDBDFlRLtkhMvKc') 
            
             #if not found   
        else:
            print(dev["name"] + " is currently OFFLINE") 
            devices_found.append(dev)
            print("Published")
            find_devices()
    return(devices_found) 


 #Start timer if device is online. After 60 minutes, send Twitter notification and run Blynk  
while True:
    now = time.time()
    if find_devices():
        if startTime==0:
            startTime = now
        timeOnline= int(now - startTime)
        print("Time online:")
        conversion = datetime.timedelta(seconds=timeOnline)
        converted_time = str(conversion)
        print (converted_time)
        if timeOnline>maxTime:
            publishTimeExpired("PS4","Online Time Expired")
            requests.get('https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key=85DHBR5KFG4SF9HH&status=PS Online')
            #run blynk warning 
            import blynk_warning #this will enable a notification to be sent to the sense hat
            
        
    else:
        startTime=0
