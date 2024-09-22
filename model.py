from time import sleep, time
import math
import os


class BinState:
    bins = ["normal", "wet", "bottle", "can"]
    enables = [True, True, True, True]

    def __init__(self, ir_sensors):
        super().__init__()
        self.ir_sensors = ir_sensors


    def update_bin_state(self):
        is_bin_full = [bool(sr.check()) for sr in self.ir_sensors]
        return is_bin_full


class Servo:
    import smbus

    def __init__(self) -> None:
        self.bus = self.smbus.SMBus(1)
        self.arduino_address = 0x55

    def write_string(self, string):
        for char in string:
            self.bus.write_byte(self.arduino_address, ord(char))  # Send ASCII value of each character
        print(f"Sent: {string}")

    def test(self):
        while True:
            self.write_string("0")
            sleep(2)
            self.write_string("1")
            sleep(2)

class Motor:
    from RpiMotorLib import RpiMotorLib
    import RPi.GPIO as GPIO

    def __init__(self, direction_pin, step_pin):
        self.GPIO.setmode(self.GPIO.BCM)

        self.direction_pin = direction_pin
        self.step_pin = step_pin

        self.stepper_motor = self.RpiMotorLib.A4988Nema(self.direction_pin, self.step_pin, (-1, -1, -1), "A4988")
        self.current_bin = 0
        

        def go(self, dir=None, hold=False):
            if dir == '>':
                self.stepper_motor.motor_go(False, "Full" , 2550, .0005, False, .05)

            elif dir == '< ': 
                self.stepper_motor.motor_go(True, "Full" , 2550, .0005, False, .05)


        def go_to_bin(self, bin_position=None, hold=False):
            if 0 <= bin_position <= 4:
                delta = bin_position - self.current_bin
                try:
                    if delta:
                        self.stepper_motor.motor_go(math.copysign(1, delta) > 0, "Full" , abs(2550 * delta), .0005, False, .05)
                        self.current_bin = bin_position

                        if not hold:
                            pass

                except:
                    pass


class Camera:
    from ultralytics import YOLO
    import numpy as np
    import cv2
    
    def __init__(self, os_type='linux', model_paths=None) -> None:
        self.os_type = os_type

        self.models = []
        for model_path in model_paths:
            model = self.YOLO(model_path)
            class_names = os.path.splitext(os.path.basename(model_path))[0].split('-')
            print(class_names)
            self.models.append((model, class_names))
        
        self.dtype = self.np.dtype([('label', 'U20'), ('confidence', 'f4')])

        if os_type == 'linux':
            from picamera2 import Picamera2

            self.picam2 = Picamera2()
            self.picam2.start()

        elif os_type == 'windows':            
            self.cap = self.cv2.VideoCapture(0)
    
    def detect(self, trial=3):
        frame = None

        if self.os_type == 'linux':
            frame = self.picam2.capture_array()

        elif self.os_type == 'windows':
            ret, frame = self.cap.read()

        frame = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
        

        prediction = self.np.array([], dtype=self.dtype)
        for i in range(trial):

            for model in self.models:
                results = model[0](frame, conf=0.5)

                for result in results:
                    detections = result.boxes

                    for det in detections:

                        prediction = self.np.append(prediction, 
                                       self.np.array(( model[1][int(det.cls[0].item())], det.conf[0].item() ), dtype=self.dtype))
                        
        print(prediction)
        return prediction


class Sensor:
    import RPi.GPIO as GPIO

    def __init__(self, pin, hold_threshold):
        self.pin = pin
        self.hold_threshold = hold_threshold
        self.sensor_start_time = None
        self.setup_gpio()

    def setup_gpio(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setup(self.pin, self.GPIO.IN)

    def check(self):
        sensor_value = not self.GPIO.input(self.pin)
        try:
            sensor_value = self.GPIO.input(self.pin)
            current_time = time()

            if sensor_value == self.GPIO.HIGH:
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
        else:
            return False


class ScoreTable:
    import numpy as np

    def __init__(self) -> None:
        self.clear()

    def calculate(self, prediction):
        label, confident = None, None
        if prediction.size > 0:
            unique_labels = self.np.unique(prediction['label'])

            total = []
            for label in unique_labels:
                confidences = prediction['confidence'][prediction['label'] == label]
                print(confidences)

                score = self.np.mean(confidences)
                total.append(score)

            scores = self.softmax(total)
            max_index = self.np.argmax(scores)

            label, confident = unique_labels[max_index], total[max_index]

            print("score =>", label, confident)

        self.prediction = prediction
        self.point = 50
        self.summary = "ขยะทั่วไป"
        self.bin = "normal"
        
        if label == "wet waste" and confident > 0.5:
            self.point = 5
            self.summary = "ขยะเปียก"
            self.bin = "wet"
        elif label == "can" and confident > 0.8: 
            self.point = 300
            self.summary = "กระป๋อง"
            self.bin = "can"
        elif label == "plastic_bottles" and confident > 0.8:
            self.point = 250
            self.summary = "ขวดพลาสติก"
            self.bin = "bottle"
        elif label == "Glass_Bottles" and confident > 0.8:
            self.point = 200
            self.summary = "ขวดแก้ว"
            self.bin = "bottle"

        return self.point


    def softmax(self, x):
        # Subtract max(x) for numerical stability
        exps = self.np.exp(x - self.np.max(x))
        return self.np.exp(x - self.np.max(x)) / self.np.sum(exps)

    def clear(self):
        self.point = None
        self.total_points = 0
        self.summary = None
        self.bin = None


class Transaction:
    import requests

    def __init__(self, api):
        self.api = api
        self.has_sent = False

    def getToken(self, path, point, prediction):
        response = self.requests.post(self.api + path, json={
            "stationId": 1,
            "point": point,
            "prediction": prediction
        })
        print("request =>", response.status_code)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data:
                url = "https://liff.line.me/2006284224-GWrYr4ey?token=" + data["token"]
                return url
        return None

    def sendNotify(self, path, binId):
        if not self.has_sent:
            try:
                response = self.requests.post(self.api + path, json={
                    "stationId": 1,
                    "binId": binId
                })
                print(response.status_code)
                if response.status_code == 200:
                    data = response.json()
                    return data
            except self.requests.exceptions.RequestException as e:
                print(f"Error sendNotify: {e}")
                return None
            

class Model:
    def __init__(self) -> None:
        self.bin_state = BinState([Sensor(pin=27, hold_threshold=5)])
        self.motor = Motor(direction_pin=17, step_pin=18)
        self.camera = Camera('windows', model_paths=["./resources/dry waste-wet waste.pt", "./resources/Glass_Bottles-can-plastic_bottles.pt"])
        self.table = ScoreTable()
        self.transaction = Transaction("https://apibkkbinplus.vercel.app")


if __name__ == '__main__':
    #x = Camera('windows', model_paths=["./resources/dry waste-wet waste.pt", "./resources/Glass_Bottles-can-plastic_bottles.pt"])
    #sleep(1)
    #x.detect()
    """
    import numpy as np
    dtype = np.dtype([('label', 'U10'), ('confidence', 'f4')])
    prediction = np.array([], dtype=dtype)
    prediction = np.append(prediction, np.array([('dog', 0.7)], dtype=dtype))
    print(prediction)
    s = ScoreTable()
    s.calculate(prediction)
    """
    x = Servo()
    x.test()
    """
    y = Sensor(27, 5)
    while(True):
        print(y.check())
        sleep(1)
    """