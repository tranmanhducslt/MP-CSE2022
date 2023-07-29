print("MQTT with Adafruit IO")
print("Sensors and Actuators")

import threading
import time
import random
import serial.tools.list_ports
import sys
from Adafruit_IO import MQTTClient
from AI import *
from voice import *
import requests

AIO_USERNAME = "multidisc2023"
AIO_KEY = "aio_bRGL44VVBaPZBJLHcx7KcPi79ePs"

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

def startAI():
    cam_thread = threading.Thread(target=pre_startAI)
    cam_thread.start()
    cam_thread.join()

def speech_recognition_loop():
    while True:
        recognized_text = recognize_speech()
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
        print("You said: " + recognized_text)

client = MQTTClient(AIO_USERNAME, AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

client.publish("info", "Welcome!")

speech_thread = threading.Thread(target=speech_recognition_loop)
speech_thread.start()

while True:
    # Execute requestData() without waiting for the speech thread to finish
    a = requestData("0")  # temp
    b = requestData("1")  # humid
    # Join the speech thread, so the loop waits until the recognition is complete
    speech_thread.join()
    time.sleep(2)