import time
import random
import sys
import json
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
from AI_oop import *
from sound_oop import *
from GPT_oop import *
from testfacedetect import *

AIO_USERNAME = "multidisc2023"
AIO_KEY = "aio_ralp78LSr2cQt4vZkZzF8G4sGmNa"
f_detect = False
p_message = True
sensor_data = {
        "humidity": 0,
        "temperature": 0,
        "t_sensor": 0,
        "h_sensor": 0,
        "fan": 0,
        "light": 0,
        "speech": 0,
        "gpt": 0
}
class AdafruitIO:
    def __init__(self):
        self.ser = None
        self.haveport = True
        self.client = MQTTClient(AIO_USERNAME, AIO_KEY)
        self.mess = ""
        self.speech_recognizer = SpeechRecognizer()
        self.recognized_text = ""
        self.speech_enabled = False
        self.face_recognition = FaceRecognition(r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\source code\images") #Use your own image folder path
        self.result = None
        self.gpt = GPT()
        self.prohibited = False

    def connected(self, c):
        print("Server connected ...")
        self.client.subscribe("button-for-light")
        self.client.subscribe("button-for-fan")
        self.client.subscribe("button-for-speech")
        self.client.subscribe("button-for-t-sensor")
        self.client.subscribe("button-for-h-sensor")
        self.client.subscribe("button-for-gpt")
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
                sensor_data["light"] = 1
                self.write_to_json()
                return
            elif payload == "0":
                print('Turn off the light...')
                self.send_command("0")
                sensor_data["light"] = 0
                self.write_to_json()
                return
        if feed_id == 'button-for-fan':
            if payload == "1":
                print("Turn on the fan...")
                self.send_command("4")
                sensor_data["fan"] = 1
                self.write_to_json()
                return
            elif payload == "0":
                print('Turn off the fan...')
                self.send_command("5")
                sensor_data["fan"] = 0
                self.write_to_json()
                return
        if feed_id == 'button-for-gpt':
            if payload == "1":
                sensor_data["gpt"] = 1
                self.write_to_json()
                print("Turn on the chatbot...")
                conversation = self.gpt.generate_response(role="user")
                print(conversation)
                time.sleep(1)
                sensor_data["gpt"] = 0
                self.write_to_json()
                print('Turning off the chatbot...')
                self.client.publish("button-for-t-sensor", "0")
                return
            elif payload == "0":
                pass   
        if feed_id == 'button-for-t-sensor':
            if payload == "1":
                sensor_data["t_sensor"] = 1
                self.write_to_json()
                print("Turn on the temperature sensor...")
                self.send_command("2")
                time.sleep(7)
                sensor_data["t_sensor"] = 0
                self.write_to_json()
                print('Turning off the temperature sensor...')
                self.client.publish("button-for-t-sensor", "0")
                return
            elif payload == "0":
                pass
        if feed_id == 'button-for-h-sensor':
            if payload == "1":
                sensor_data["h_sensor"] = 1
                self.write_to_json()
                print("Turn on the heat sensor...")
                self.send_command("3")
                time.sleep(7)
                sensor_data["h_sensor"] = 0
                self.write_to_json()
                print('Turning off the heat sensor...')
                self.client.publish("button-for-h-sensor", "0")
                return
            elif payload == "0":
                pass
        if feed_id == 'button-for-speech':
            if payload == "1" and not self.speech_enabled:
                self.speech_enabled = True
                sensor_data["speech"] = 1
                self.write_to_json()
                print("Speech recognition on...")
                self.recognized_text = self.speech_recognizer.recognize_speech().capitalize()
                if self.recognized_text == "Fan on":
                    self.send_command("4")
                elif self.recognized_text == "Fan off":
                    self.send_command("5")
                elif self.recognized_text == "Light on":
                    self.send_command("1")
                elif self.recognized_text == "Light off":
                    self.send_command("0")
                print("You can turn it off now...")
                time.sleep(1)
                return
            elif payload == "0":
                sensor_data["speech"] = 0
                self.write_to_json()
                print('Speech recognition off...')
                self.speech_enabled = False
                return
    #    print("Testing commands")
    
    def send_command(self, cmd):
        if self.haveport:
            self.ser.write(cmd.encode())

    def info(self, message):
        if message is not None:
            self.client.publish("info", message)

    def process_data(self, data):
        global hu, temp
        print(data)
        data = data.replace("!", "")
        data = data.replace("#", "")
        split_data = data.split(":")
        print(split_data)
        if split_data[1] == "T":
            temp = split_data[2]
            self.client.publish("Temp", split_data[2])
            sensor_data["temperature"] = float(split_data[2])
            self.write_to_json()
            if float(split_data[2]) < 26:
                self.client.publish("info", "Too cold - Please increase temp. to [26-28] Celsius after checking plant")
                self.send_command("4")
            elif float(split_data[2]) > 28:
                self.client.publish("info", "Too hot - Please decrease temp. to [26-28] Celsius after checking plant")
                self.send_command("4")
            else:
                self.send_command("5")

        elif split_data[1] == "H":
            hu = split_data[2]
            self.client.publish("Humid", split_data[2])
            sensor_data["humid"] = float(split_data[2])
            self.write_to_json()
            if float(split_data[2]) < 50:
                self.client.publish("info", "Too dry - Please increase humid. to [50-70] per cent after checking plant")
                self.send_command("1")
            elif float(split_data[2]) > 70:
                self.client.publish("info", "Too humid - Please decrease humid. to [50-70] per cent after checking plant")
                self.send_command("1")
            else:
                self.send_command("0")


    def write_to_json(self):
        global sensor_data
        file_path = r"C:\Users\Minecrap\Desktop\MP-CSE2022-main\sensor_data.json"

        with open(file_path, "w") as json_file:
            json.dump(sensor_data, json_file)

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

    def face_detection_l(self):
        if self.face_recognition.result == 'e':
            print("Access granted.")
        elif self.face_recognition.result == 's':
            print("Access denied.")
            time.sleep(0.75)
            sys.exit(1)
        else:
            print("Access denied.")
            time.sleep(0.75)
            sys.exit(1)

    def start(self):
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe

        global f_detect, p_message

        self.write_to_json()
        self.face_recognition.start_human()
        time.sleep(3)
        if f_detect == False:
            self.face_detection_l()
            f_detect = True
        
        self.client.connect()
        self.client.loop_background()
        
        self.client.publish("info", "Welcome, Engineer!")

        try:
            self.ser = serial.Serial(port="COM4", baudrate=115200)
            print("Port found")
        except:
            self.haveport = False
            print("Cannot open the port")

        while True:
            cam = Camera()
            cam.startAI()
            time.sleep(1)
            if p_message:
                if cam.message is not None and isinstance(cam.message, str):
                    self.info(cam.message)
                p_message = False
            if self.haveport:
                self.request_data("0")  # temp
                self.request_data("1")  # humid
            else:  # no ports plugged in
                x1 = random.randint(2600, 2800) / 100
                x2 = random.randint(5000, 7000) / 100
                self.client.publish("Temp", x1)
                self.client.publish("Humid", x2)

if __name__ == "__main__":  # for testing purposes
    adafruit_io = AdafruitIO()
    adafruit_io.start()
