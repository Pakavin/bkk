import smbus
import time

bus = smbus.SMBus(1)
arduino_address = 0x55

def write_string(string):
    for char in string:
        bus.write_byte(arduino_address, ord(char))  # Send ASCII value of each character
    print(f"Sent: {string}")

while True:
    write_string("0")  # Send a string
    time.sleep(2)
    write_string("1")
    time.sleep(2)
