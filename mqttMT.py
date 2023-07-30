print("MQTT with Adafruit IO")
print("Sensors and Actuators")

import threading
import time
import random
import serial.tools.list_ports
import sys
import requests
from Adafruit_IO import MQTTClient
from AI import *
from sound import *

AIO_USERNAME = "multidisc2023"
AIO_KEY = "aio_WWqu758Y2dR8fJKjCM7qAS5YHz8y"

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
    haveport = True
except:
    print("Cannot open the port")
    haveport = False

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
        if float(splitData[2]) < 5:
            infor("Too cold")
            sendCommand("4")
            infor(startAI())
        elif float(splitData[2]) > 15:
            infor("Too hot")
            sendCommand("4")
            infor(startAI())
        else:
            sendCommand("5")
            pass
    
    elif splitData[1] == "H":
        client.publish("Humid", splitData[2])
        if float(splitData[2]) < 75:
            infor("Too dry")
            sendCommand("2")
            infor(startAI())
        elif float(splitData[2]) > 90:
            infor("Too humid")
            sendCommand("2")
            infor(startAI())
        else:
            sendCommand("3")
            pass

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

def speech_recognition_loop():
    global recognized_text
    while True:
        recognized_text = recognize_speech()
        if recognized_text is not None:
            if recognized_text == "Fan on":
                sendCommand("2")
                return
            elif recognized_text == "Fan off":
                sendCommand("3")
                return
            if recognized_text == "Light on":
                sendCommand("4")
                return
            elif recognized_text == "Light off":
                sendCommand("5")
                return
        
client = MQTTClient(AIO_USERNAME, AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

client.publish("info", "Welcome!")

speech_thread = threading.Thread(target = speech_recognition_loop)
speech_thread.start()

while True:
    time.sleep(2)
    if haveport:
        # execute requestData() without waiting for the speech thread to finish
        a = requestData("0")  # temp
        b = requestData("1")  # humid
    else: # testing without hardware, no breaching
        x1 = random.randint(500, 1500) / 100
        x2 = random.randint(7500, 9000) / 100
        client.publish("Temp", x1)
        client.publish("Humid", x2)
    pass