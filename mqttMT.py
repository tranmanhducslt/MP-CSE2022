print("MQTT with Adafruit IO")
print("Sensors and Actuators")

import time
import random
import serial.tools.list_ports
import sys
from Adafruit_IO import MQTTClient
from AI import *
from sound import *
import requests
# import sensor

AIO_USERNAME = "multidisc2023"
AIO_KEY = "aio_bRGL44VVBaPZBJLHcx7KcPi79ePs"

global_equation = "x1 + x2 + x3"


def init_global_equation():
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/multidisc2023/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()


def connected(client):
    print("Server connected ...")
    client.subscribe("button-for-light")
    client.subscribe("button-for-fan")
    client.subscribe("info")

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed!")


def disconnected(client):
    print("Disconnected from the server!")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Received: " + payload)
    if feed_id == 'button-for-fan':
        if payload == "1":
            print("Turn on the device...")
            sendCommand("2")
            return
        elif payload == "0":
            print('Turn off the device...')
            sendCommand("3")
            return
    if feed_id == 'button-for-light':
        if payload == "1":
            print("Turn on the device...")
            sendCommand("4")
            return
        elif payload == "0":
            print('Turn off the device...')
            sendCommand("5")
            return
    print("Testing commands")


try:
    ser = serial.Serial(port="COM4", baudrate=115200)
except:
    print("Cannot open the port")
    exit()

def sendCommand(cmd):
    ser.write(cmd.encode())

def infor(message): # print to terminal and feed
    if message is not None:
        print(message)
        client.publish("info", message)

mess = ""

def processData(data):
    print(data)
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "T":
        client.publish("Temp", splitData[2])
        if float(splitData[2]) < 25:
            infor("Too cold")
            sendCommand("4")
            infor(startAI())
        elif float(splitData[2]) > 30:
            infor("Too hot")
            sendCommand("4")
            infor(startAI())
        else:
            sendCommand("5")
    
    elif splitData[1] == "H":
        client.publish("Humid", splitData[2])
        if float(splitData[2]) < 40:
            infor("Too dry")
            sendCommand("2")
            infor(startAI())
        elif float(splitData[2]) > 70:
            infor("Too humid")
            sendCommand("2")
            infor(startAI())
        else:
            sendCommand("3")

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def requestData(cmd):
    sendCommand(cmd)
    time.sleep(1)
    readSerial()


client = MQTTClient(AIO_USERNAME, AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()
init_global_equation()

client.publish("info", "Welcome!")
while True:
    a = requestData("0") # temp
    b = requestData("1") # humid    
    time.sleep(2)
    pass