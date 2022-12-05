"""
MicroPython IoT Weather Station Example for Wokwi.com

To view the data:

1. Go to http://www.hivemq.com/demos/websocket-client/
2. Click "Connect"
3. Under Subscriptions, click "Add New Topic Subscription"
4. In the Topic field, type "wokwi-weather" then click "Subscribe"

Now click on the DHT22 sensor in the simulation,
change the temperature/humidity, and you should see
the message appear on the MQTT Broker, in the "Messages" pane.

Copyright (C) 2022, Uri Shaked

https://wokwi.com/arduino/projects/322577683855704658
"""

import network
import time
from machine import Pin,Timer
import dht
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_BROKER2='broker.emqx.io'
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "sensor"
s1_state=False
s2_state=False
s3_state=False
timer=Timer(0)
sensor = dht.DHT22(Pin(15))
livingroom=Pin(25,Pin.OUT)
bedroom=Pin(26,Pin.OUT)
bathroom=Pin(27,Pin.OUT)

def publish_data(t):
  sensor.measure()
  message={'tempreture':sensor.temperature(),
  'humidity':sensor.humidity()}
  print(message)
  message=ujson.dumps(message)
  client.publish(MQTT_TOPIC,message)

def get_message(topic,msg):
  state=msg.decode()
  if state=='livingroom-on':
    livingroom.on()
  if state=='livingroom-off':
    livingroom.off()
  if state=='bathroom-on':
    bathroom.on()
  if state=='bathroom-off':
    bathroom.off()
  if state=='bedroom-on':
    bedroom.on()
  if state=='bedroom-off':
    bedroom.off()
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER2, user=None, password=None,port=1883)
client.connect()
client.set_callback(get_message)
print("Connected!")
client.subscribe("test/lights")
timer.init(period=4000,mode=Timer.PERIODIC,callback=lambda t:publish_data(t))
while True:
  client.check_msg()
  time.sleep(0.2)

