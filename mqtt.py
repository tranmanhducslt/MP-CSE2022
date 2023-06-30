import sys
import time
import random
import requests
from Adafruit_IO import MQTTClient
AIO_USERNAME = "tranmanhducslt"
AIO_KEY = "aio_xpYz27A2GrCpMePrNLJvybOISRVP"
global_equation = "x1 + x2 + x3"

def init_global_equation():
    global global_equation
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/tranmanhducslt/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global_equation = data["last_value"]
    print("Get latest value:", global_equation)

def connected(client):
    print("Server connected ...")
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("equation")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!")

def disconnected(client):
    print("Disconnected from the server!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload)
    if (feed_id == "equation"):
        global global_equation
        global_equation = payload
        print(global_equation)

def modify(x1, x2, x3):
    global global_equation
    result = eval(global_equation)
    return result

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected # function pointer/callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
# meaning: .on_cue = call function

client.connect()
client.loop_background()
init_global_equation()

while True:
    time.sleep(10) # updating every interval
    client.publish("sensor1", random.randint(25, 40))
    client.publish("sensor2", random.randint(60, 80))
    client.publish("sensor3", random.randint(60, 80)/10)
    print(modify(random.randint(1,10), random.randint(1,10), random.randint(1,10)))