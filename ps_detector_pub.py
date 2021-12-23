import subprocess
#from BlynkLib import Blynk
import paho.mqtt.client as mqtt
import time
from sense_hat import SenseHat
import paho.mqtt.publish as publish
from urllib.parse import urlparse
import sys


devices = [{"name":"Jude's PS4", "mac":"A4:FC:77:FD:BD:59"}]

#initialise SenseHAT
sense = SenseHat()
sense.clear()

url_str = sys.argv[1]
print(url_str)
url = urlparse(url_str)

base_topic = url.path[1:]

mqttc = mqtt.Client()

# Returns the list of known devices found on the network
def find_devices():
    output = subprocess.check_output("sudo nmap -sn 192.168.1.0/24 | grep MAC", shell=True)
    devices_found=[]
    for dev in devices:   
        if dev["mac"].lower() in str(output).lower():
            print(dev["name"] + " is currently ONLINE")
            devices_found.append(dev)
            mqttc.publish(base_topic+"/Device Online")
            print("Published")
        
        else:
            print(dev["name"] + " is currently OFFLINE") 
            mqttc.publish(base_topic+"/Device Offline")
            print("Published")
    return(devices_found)

if (url.username):
    mqttc.username_pw_set(url.username, url.password)

mqttc.connect(url.hostname, url.port)
mqttc.loop_start()

def job():
    print("ps detetcor running...")

def main():
   #subprocess.call("Blynk.run", shell=True)
   (job(), find_devices())
  
   
if __name__ == "__main__":
   main()

while True:
  main()
  #schedule.every(60).seconds.do(main)
  time.sleep (60)

