import sys
from Adafruit_IO import MQTTClient


AIO_FEED_ID = ""
AIO_USERNAME = ""
AIO_KEY = ""
def connected(client):
    print("Connected to server!!!")
    client.subscribe(AIO_FEED_ID)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed successfully...")

def disconnected(client):
    print("Disconnected from server!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received data: " + payload)
