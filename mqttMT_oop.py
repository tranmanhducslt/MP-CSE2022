import threading
import time
import datetime
import random
import sys
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
from AI_oop import *
from sound_oop import *
from GPT_oop import *
from testfacedetect import *

AIO_USERNAME = "multidisc2023"
AIO_KEY = "aio_WxGV19DXtOXpqtsOCYdwKsmKF1Co"
f_detect = True

class AdafruitIO:
    def __init__(self):
        self.ser = None
        self.haveport = True
        self.client = MQTTClient(AIO_USERNAME, AIO_KEY)
        self.mess = ""
        self.speech_recognizer = SpeechRecognizer()
        self.recognized_text = ""
        self.speech_enabled = False
        self.face_recognition = FaceRecognition(r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\source code\images")
        self.result = None

    def connected(self, c):
        print("Server connected ...")
        self.client.subscribe("button-for-light")
        self.client.subscribe("button-for-fan")
        self.client.subscribe("button-for-speech")
        self.client.subscribe("button-for-t-sensor")
        self.client.subscribe("button-for-h-sensor")
        self.client.subscribe("info")

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed!")

    def disconnected(self, client):
        print("Disconnected from the server!")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Received: " + payload)
        if feed_id == 'button-for-light':
            if payload == "1":
                print("Turn on the light...")
                self.send_command("1")
                return
            elif payload == "0":
                print('Turn off the light...')
                self.send_command("0")
                return
        if feed_id == 'button-for-fan':
            if payload == "1":
                print("Turn on the fan...")
                self.send_command("4")
                return
            elif payload == "0":
                print('Turn off the fan...')
                self.send_command("5")
                return
        if feed_id == 'button-for-t-sensor':
            if payload == "1":
                print("Turn on the temperature sensor...")
                self.send_command("2")
                print('Turning off...')
                time.sleep(5)
                self.client.publish("button-for-t-sensor", "0")
                return
            elif payload == "0":
                pass
        if feed_id == 'button-for-h-sensor':
            if payload == "1":
                print("Turn on the heat sensor...")
                self.send_command("3")
                print('Turning off...')
                time.sleep(5)
                self.client.publish("button-for-h-sensor", "0")
                return
            elif payload == "0":
                pass
        if feed_id == 'button-for-speech':
            if payload == "1" and not self.speech_enabled:
                self.speech_enabled = True
                print("Speech recognition on...")
                self.recognized_text = self.speech_recognizer.recognize_speech()
                if str(self.recognized_text) == "Fan on":
                    self.send_command("4")
                elif str(self.recognized_text) == "Fan off":
                    self.send_command("5")
                elif str(self.recognized_text) == "Light on":
                    self.send_command("1")
                elif str(self.recognized_text) == "Light off":
                    self.send_command("0")
                print("You can turn it off now...")
                time.sleep(2)
                return
            elif payload == "0":
                print('Speech recognition off...')
                self.speech_enabled = False
                return
    #    print("Testing commands")
    
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
            self.client.publish("Temp", split_data[2])
            if float(split_data[2]) < 26:
                self.info("Too cold - Please increase temperature to [26-28] Celsius after checking plant")
                self.send_command("4")
            elif float(split_data[2]) > 28:
                self.info("Too hot - Please decrease temperature to [26-28] Celsius after checking plant")
                self.send_command("4")
            else:
                self.send_command("5")

        elif split_data[1] == "H":
            self.client.publish("Humid", split_data[2])
            if float(split_data[2]) < 50:
                self.info("Too dry - Please increase humidity to [50-70] per cent after checking plant")
                self.send_command("1")
            elif float(split_data[2]) > 70:
                self.info("Too humid - Please decrease humidity to [50-70] per cent after checking plant")
                self.send_command("1")
            else:
                self.send_command("0")

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

    def speech_recognition_loop(self):
        self.recognized_text = self.speech_recognizer.recognize_speech()
        if str(self.recognized_text) == "Fan on":
            self.send_command("4")
        elif str(self.recognized_text) == "Fan off":
            self.send_command("5")
        elif str(self.recognized_text) == "Light on":
            self.send_command("1")
        elif str(self.recognized_text) == "Light off":
            self.send_command("0")

    def face_detection_l(self):
        result = self.face_recognition.recognition()
        time_detection = datetime.datetime.now()

        if result == 'e':
            starttime = datetime.datetime.now()
            if (datetime.datetime.now() - starttime).total_seconds() == 2 and result == 'e':
                self.client.publish("info", "Greetings, engineer!")
            else:
                print("Invalid detection.")

        elif result == 's':
            starttime = datetime.datetime.now()
            if (datetime.datetime.now() - starttime).total_seconds() == 2 and result == 's':
                self.client.publish("info", "No strangers intervened!")
            else:
                print("Invalid detection.")

        else:
            if (datetime.datetime.now() - time_detection).total_seconds() == 15: #if no one's detected on the camera within 20 seconds, the camera detection stops
                print("No detection found.")

        self.face_recognition.cap.release()
        cv2.destroyAllWindows()

    def start(self):
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()
        self.client.publish("info", "Welcome!")
        
        try:
            self.ser = serial.Serial(port="COM4", baudrate=115200)
            print("Port found")
        except:
            self.haveport = False
            print("Cannot open the port")

        while True:
            global f_detect
            if f_detect:
                self.face_detection_l()
                f_detect = False
                time.sleep(20)
                cv2.destroyAllWindows()
            time.sleep(3)
            cam = Camera()
            if cam.startAI():
                pass
            if self.haveport:
                self.request_data("0")  # temp
                self.request_data("1")  # humid
                time.sleep(1)
            else:  # no ports plugged in
                x1 = random.randint(2600, 2800) / 100
                x2 = random.randint(5000, 7000) / 100
                self.client.publish("Temp", x1)
                self.client.publish("Humid", x2)

if __name__ == "__main__":  # for testing purposes
    adafruit_io = AdafruitIO()
    adafruit_io.start()