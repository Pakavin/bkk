import RPi.GPIO as GPIO
import time

class Sensor:
    def __init__(self, pin, hold_threshold):
        self.pin = pin
        self.hold_threshold = hold_threshold
        self.sensor_start_time = None
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def check(self):
        try:
            sensor_value = GPIO.input(self.pin)
            return sensor_value
            print(f"{self.pin} =>", sensor_value)
            current_time = time.time()

            if sensor_value == GPIO.HIGH:
                if self.sensor_start_time is None:
                    self.sensor_start_time = current_time
            else:
                if self.sensor_start_time is not None:
                    hold_duration = current_time - self.sensor_start_time
                    if hold_duration >= self.hold_threshold:
                        self.sensor_start_time = None
                        return True
                    self.sensor_start_time = None  # Reset after release
            return False
        except:
            return False

class IRSensor(Sensor):
    def __init__(self, pin=None, hold_threshold=60):
        super().__init__(pin, hold_threshold)

    def check(self):
        sensor_value = not GPIO.input(self.pin)
        return sensor_value
        try:
            sensor_value = GPIO.input(self.pin)
            print(f"{self.pin} =>", sensor_value)
            current_time = time.time()

            if sensor_value == GPIO.HIGH:
                if self.sensor_start_time is None:
                    self.sensor_start_time = current_time

                if self.sensor_start_time is not None:
                    hold_duration = current_time - self.sensor_start_time
                    if hold_duration >= self.hold_threshold:
                        return True
            else:
                self.sensor_start_time = None
        except:
            pass
    
class MagneticSwitch(Sensor):
    def __init__(self, pin=None, hold_threshold=60):
        super().__init__(pin, hold_threshold)
        
if __name__ == '__main__':
    # sensors = [IRSensor(27), IRSensor(22), IRSensor(23), IRSensor(24)]
    # while(True):
    #     for sr in sensors:
    #         sr.update_value()
    #          print(f"{sr.pin} => {'1' if sr.value else '0'}")
    #     print()
    #     sleep(1)

    magnetic = MagneticSwitch(26)
    #ir = IRSensor(23, None)
    while True:
        magnetic.check()
        #ir.check()
        time.sleep(0.5)
