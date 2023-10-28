import threading
import time
import random
import sys
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
from AI_oop import *
from sound_oop import *

AIO_USERNAME = "multidisc2023"
AIO_KEY = "aio_XkKj27e3qwROBd81fj5oBXJkG9ap"

class AdafruitIO:
    def __init__(self):
        self.client = MQTTClient(AIO_USERNAME, AIO_KEY)
        self.haveport = False
        self.mess = ""

    def connected(self, client):
        print("Server connected ...")
        client.subscribe("button-for-light")
        client.subscribe("button-for-fan")
        client.subscribe("info")

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
                self.send_command("2")
                return
            elif payload == "0":
                print('Turn off the device...')
                self.send_command("3")
                return
        if feed_id == 'button-for-light':
            if payload == "1":
                print("Turn on the device...")
                self.send_command("4")
                return
            elif payload == "0":
                print('Turn off the device...')
                self.send_command("5")
                return
        print("Testing commands")

    def send_command(self, cmd):
        if self.haveport:
            ser.write(cmd.encode())

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
            cam = Camera()
            self.client.publish("Temp", split_data[2])
            if float(split_data[2]) < 5:
                self.info("Too cold")
                self.send_command("4")
                self.info(cam.startAI())
            elif float(split_data[2]) > 15:
                self.info("Too hot")
                self.send_command("4")
                self.info(cam.startAI())
            else:
                self.send_command("5")

        elif split_data[1] == "H":
            self.client.publish("Humid", split_data[2])
            if float(split_data[2]) < 75:
                self.info("Too dry")
                self.send_command("2")
                self.info(cam.startAI())
            elif float(split_data[2]) > 90:
                self.info("Too humid")
                self.send_command("2")
                self.info(cam.startAI())
            else:
                self.send_command("3")

    def read_serial(self):
        bytes_to_read = ser.inWaiting()
        if bytes_to_read > 0:
            self.mess = self.mess + ser.read(bytes_to_read).decode("UTF-8")
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
        self.read_serial()

    def speech_recognition_loop(self):
        global recognized_text
        while True:
            speech_recognizer = SpeechRecognizer()
            if speech_recognizer.recognize_speech() is not None:
                recognized_text = speech_recognizer.recognize_speech()
                if recognized_text == "Fan on":
                    self.send_command("2")
                    return
                elif recognized_text == "Fan off":
                    self.send_command("3")
                    return
                if recognized_text == "Light on":
                    self.send_command("4")
                    return
                elif recognized_text == "Light off":
                    self.send_command("5")
                    return

    def start(self):
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()

        self.client.publish("info", "Welcome!")

        speech_thread = threading.Thread(target=self.speech_recognition_loop)
        speech_thread.start()

        while True:
            time.sleep(2)
            if self.haveport:
                a = self.request_data("0")  # temp
                b = self.request_data("1")  # humid
            else:
                x1 = random.randint(500, 1600) / 100
                x2 = random.randint(7500, 9600) / 100
                self.client.publish("Temp", x1)
                self.client.publish("Humid", x2)

if __name__ == "__main__": #For testing purpose
    adafruit_io = AdafruitIO()
    try:
        ser = serial.Serial(port="COM4", baudrate=115200)
        adafruit_io.haveport = True
    except Exception as e:
        print("Cannot open the port:", e)

    adafruit_io.start()