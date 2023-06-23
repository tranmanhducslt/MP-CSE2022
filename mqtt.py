import sys
import time
import random
from Adafruit_IO import MQTTClient
AIO_USERNAME = "tranmanhducslt"
AIO_KEY = ""

def connected(client):
    print("Server connected ...")
    client.subscribe("button1")
    client.subscribe("button2")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!")

def disconnected(client):
    print("Disconnected from the server!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected # function pointer/callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
# meaning: on_cue = call function

client.connect()
client.loop_background()

while True:
    time.sleep(10) # updating every interval
    client.publish("sensor1", random.randint(25, 35))
    client.publish("sensor2", random.randint(60, 85))
    client.publish("sensor3", random.randint(60, 85)/10)
    pass