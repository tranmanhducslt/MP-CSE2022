import time
import serial.tools.list_ports

print("Sensors and Actuators")
try:
    ser = serial.Serial(port="COM3", baudrate=115200)
except:
    print("Cannot open the port")

def sendCommand(cmd):
    ser.write(cmd.encode())

def requestData(cmd, client):
    sendCommand(cmd)

mess = ""
def processData(data, client):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    print(client)

def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1], client)
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
'''
while True:
    print("Testing commands")
    for i in range(0, 6):
        sendCommand(str(i))
        time.sleep(2) # relay: switcher for low-power devices
'''