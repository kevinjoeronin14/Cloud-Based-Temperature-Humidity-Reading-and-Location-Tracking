import RPi.GPIO as GPIO
import dht11
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
Kevin Joe Ronin
Cloud Based Temperature , Humidity Reading and Location Tracking
import json
organization = "*organization name"
deviceType = "*device type"
deviceId = "*device id"
authMethod = "token"
authToken = "*authtoken"
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
SensorInstance = dht11.DHT11(pin = 13) # read data using pin 13
# Initialize the device client.
T=0
H=0
def myCommandCallback(cmd):
 print("Command received: %s" % cmd.data['command'])
 GPIO.setup(7,GPIO.OUT)
 if cmd.data['command']=='lighton':
 print("LIGHT ON IS RECEIVED")
 GPIO.output(7,1)

 elif cmd.data['command']=='lightoff':
 GPIO.output(7,0)
 print("LIGHT OFF IS RECEIVED")
 if cmd.command == "setInterval":
Cloud Based Temperature , Humidity Reading and Location Tracking
 if 'interval' not in cmd.data:
 print("Error 'interval'")
 else:
 interval = cmd.data['interval']
 elif cmd.command == "print":
 if 'message' not in cmd.data:
 print("Error 'message'")
 else:
 print(cmd.data['message'])
try:
 deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "authtoken": authToken}
 deviceCli = ibmiotf.device.Client(deviceOptions)

except Exception as e:
 print("Caught exception connecting device: %s" % str(e))
 sys.exit()
deviceCli.connect()
while True:
 #Get Sensor Data from DHT11
 SensorData = SensorInstance.read()
 if SensorData.is_valid():
 #if True:
 T = SensorData.temperature
 H = SensorData.humidity
 else:
 print ("SensorData Invalid")
 #Send Temperature & Humidity to IBM Watson
Cloud Based Temperature , Humidity Reading and Location Tracking
 data = {"d":{ 'temperature' : T, 'humidity': H }}
 #print data
 def myOnPublishCallback():
 print ("Published Temperature = %s C" % T, "Humidity = %s %%" % H, "to IBM Watson")
 success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
 if not success:
 print("Not connected to IoTF")
 time.sleep(1)
 deviceCli.commandCallback = myCommandCallback
deviceCli.disconnect()
