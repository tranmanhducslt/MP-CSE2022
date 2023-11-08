import threading
import time
import random
import sys
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
from AI_oop import *
from sound_oop import *
from GPT_oop import *

AIO_USERNAME = "multidisc2023"
AIO_KEY = "aio_iEgl61ZYLiOnJs0fAMQvG7FRrc05"

class AdafruitIO:
    def __init__(self):
        self.ser = None
        self.haveport = True
        self.client = MQTTClient(AIO_USERNAME, AIO_KEY)
        self.mess = ""
        self.speech_recognizer = SpeechRecognizer()
        self.recognized_text = None
        self.speech_enabled = False

    def connected(self, c):
        print("Server connected ...")
        self.client.subscribe("button-for-light")
        self.client.subscribe("button-for-fan")
        self.client.subscribe("button-for-speech")
        self.client.subscribe("info")

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed!")

    def disconnected(self, client):
        print("Disconnected from the server!")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Received: " + payload)
        if feed_id == 'button-for-fan':
            if payload == "1":
                print("Turn on the device...")
                self.send_command("4")
                return
            elif payload == "0":
                print('Turn off the device...')
                self.send_command("5")
                return
        if feed_id == 'button-for-light':
            if payload == "1":
                print("Turn on the device...")
                self.send_command("1")
                return
            elif payload == "0":
                print('Turn off the device...')
                self.send_command("0")
                return
        if feed_id == 'button-for-speech':
            if payload == "1" and not self.speech_enabled:
                self.speech_enabled = True
                print("Speech recognition on...")
                self.speech_recognizer.enable_recognition()
                self.speech_recognition_loop(self.speech_enabled)
                self.speech_recognizer.disable_recognition()
                print("You can turn it off now...")
                time.sleep(3)
            elif payload == "0":
                print('Speech recognition off...')
                self.speech_enabled = False
    #    print("Testing commands")
    
    def check_port(self):
        try:
            self.ser = serial.Serial(port="COM4", baudrate=115200)
            return True
        except:
            print("Cannot open the port")
            return False

    def send_command(self, cmd):
        if self.haveport:
            self.ser.write(cmd.encode())

    def info(self, message):
        if message is not None:
            print(message)
            self.client.publish("info", message)

    def process_data(self, data):
        print(data)
        data = data.replace("!", "")
        data = data.replace("#", "")
        split_data = data.split(":")
        print(split_data)
        if split_data[1] == "T":
            cam = Camera(0)
            self.client.publish("Temp", split_data[2])
            if float(split_data[2]) < 26:
                self.info("Too cold")
                self.send_command("2")
                self.info(cam.startAI())
            elif float(split_data[2]) > 28:
                self.info("Too hot")
                self.send_command("2")
                self.info(cam.startAI())
            else:
                self.send_command("3")

        elif split_data[1] == "H":
            cam = Camera(0)
            self.client.publish("Humid", split_data[2])
            if float(split_data[2]) < 50:
                self.info("Too dry")
                self.send_command("4")
                self.info(cam.startAI())
            elif float(split_data[2]) > 70:
                self.info("Too humid")
                self.send_command("4")
                self.info(cam.startAI())
            else:
                self.send_command("5")

    def read_serial(self, client):
        bytes_to_read = self.ser.inWaiting()
        if bytes_to_read > 0:
            self.mess = self.mess + self.ser.read(bytes_to_read).decode("UTF-8")
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                self.process_data(self.mess[start:end + 1])
                if end == len(self.mess):
                    self.mess = ""
                else:
                    self.mess = self.mess[end+1:]

    def request_data(self, cmd):
        self.send_command(cmd)
        time.sleep(1)
        self.read_serial(self.client)

    def speech_recognition_loop(self, cond):
        if self.speech_recognizer.recognize_speech() is not None and cond:
            self.recognized_text = self.speech_recognizer.recognize_speech()
            if self.recognized_text == "Fan on":
                self.send_command("2")
            elif self.recognized_text == "Fan off":
                self.send_command("3")
            elif self.recognized_text == "Light on":
                self.send_command("4")
            elif self.recognized_text == "Light off":
                self.send_command("5")
        else:
            pass

    def start(self):
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()

        self.client.publish("info", "Welcome!")
        self.haveport = self.check_port()

        cam = Camera(1)
        cam.startAI()
        

        while True:
            time.sleep(2)
            if self.haveport:
                a = self.request_data("0")  # temp
                b = self.request_data("1")  # humid
            else:  # no ports plugged in
                x1 = random.randint(2600, 2800) / 100
                x2 = random.randint(5000, 7000) / 100
                self.client.publish("Temp", x1)
                self.client.publish("Humid", x2)

if __name__ == "__main__":  # for testing purposes
    adafruit_io = AdafruitIO()
    adafruit_io.start()