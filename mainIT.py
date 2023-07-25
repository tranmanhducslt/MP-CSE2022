import sys
import time
import random
from Adafruit_IO import MQTTClient
import requests
import warnings
AIO_USERNAME = "tranmanhducslt"
AIO_KEY = "aio_Bhpn14IudeTPXHSv6HZng13vx1i6"
equation= 'x1+x2+x3+x4'
sum_count = False
warnings.filterwarnings("ignore")
def init_global_equation():
    global global_equation
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/tranmanhducslt/feeds/sum"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global_equation = "x1+x2+x3+x4"
    print("Get lastest value:", global_equation)
def modify_value(x1,x2,x3,x4):
    result= eval(equation)
    print(result)
    return result

def connected(client):
    print("Server connected ...")
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("equation")
    client.subscribe("pricecoffee")
    client.subscribe("sensor1")
    client.subscribe("sensor2")
    client.subscribe("sensor3")
    client.subscribe("sum")
def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!")

def disconnected(client):
    print("Disconnected from the server!")
    sys.exit (1)

def message(client , feed_id , payload):
    global sum_count
    print("Received: " + payload)
    if feed_id == "buttontrade":
        if payload == "1":
            sum_count = True
        elif payload == "0":
            sum_count = False

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected # function pointer/callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
# meaning: on_cue = call function

client.connect()
client.loop_background()

global_equation = 'x1+x2+x3+x4'
init_global_equation()

while True:
    time.sleep(10) # updating every interval
    x1 = random.randint(-500, 6000)
    x2 = random.randint(-25, 175)
    x3 = random.randint(-500, 2500)
    x4 = random.randint(-10, 80)
    #x = random.randint(0, 1)
    result = modify_value(x1, x2, x3, x4)


    client.publish("sensor1", x1)
    client.publish("sensor2", x2)
    client.publish("sensor3", x3)
    client.publish("pricecoffee", x4)
    if sum_count:
        client.publish("sum", result)
