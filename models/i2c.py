import smbus
import time

bus = smbus.SMBus(1)
arduino_address = 0x08

def write_string(string):
    for char in string:
        bus.write_byte(arduino_address, ord(char))  # Send ASCII value of each character
    print(f"Sent: {string}")

if __name__ == '__main__':
    while True:
        write_string("on")
        time.sleep(1)
        write_string("off")
        time.sleep(1)
