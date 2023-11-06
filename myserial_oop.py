import time
import serial.tools.list_ports

class SensorActuator:
    def __init__(self, port="COM4", baudrate=115200):
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate)
            self.mess = ""
        except Exception as e:
            print(f"Cannot open the port: {e}")

    def send_command(self, cmd):
        self.ser.write(cmd.encode())

    def process_data(self, data, client):
        data = data.replace("!", "")
        data = data.replace("#", "")
        split_data = data.split(":")
        print(split_data)
        print(client)  # You can use the client as needed

    def read_serial(self, client):
        bytes_to_read = self.ser.inWaiting()
        if bytes_to_read > 0:
            self.mess = self.mess + self.ser.read(bytes_to_read).decode("UTF-8")
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                self.process_data(self.mess[start:end + 1], client)
                if end == len(self.mess):
                    self.mess = ""
                else:
                    self.mess = self.mess[end+1:]

if __name__ == "__main__": #For testing purpose
    sensor_actuator = SensorActuator()

    while True:
        # Replace the command and client with your specific logic
        command = "your_command"
        client = "your_client"

        sensor_actuator.send_command(command)
        sensor_actuator.read_serial(client)
        time.sleep(2)