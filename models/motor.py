from RpiMotorLib import RpiMotorLib
from threading import Thread
import RPi.GPIO as GPIO
from time import sleep
import pigpio
import pickle
import math
import os


class Servo(Thread):
    def __init__(self, pin):
        super().__init__()
        self.pin = pin

        self.pwm = pigpio.pi()
        self.pwm.set_mode(pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(pin, 50)

    def drive(self, pwm):
        self.pwm.hardware_PWM(self.pin, 50, pwm)


class Motor:
    def __init__(self, direction_pin, step_pin, file_path, servo_pin):
        GPIO.setmode(GPIO.BCM)

        self.direction_pin = direction_pin
        self.step_pin = step_pin

        self.stepper_motor = RpiMotorLib.A4988Nema(self.direction_pin, self.step_pin, (-1, -1, -1), "A4988")
        self.stepdelay = .0005

        self.file_path = file_path

        self.servo = Servo(servo_pin) 
        self.servo.drive(60000)

        if os.path.exists(self.file_path):
            with open(self.file_path, "rb") as f:
                self.current_bin = pickle.load(f)
        else:
            self.current_bin = 3

    def go(self, dir):
        if dir == 'backward':
            self.stepper_motor.motor_go(False, "Full" , 2550, .0005, False, .05)
        elif dir == 'forward': 
            self.stepper_motor.motor_go(True, "Full" , 2550, .0005, False, .05)

    def go_to_bin(self, bin_position=None, hold=False):
        if 0 <= bin_position <= 4:
            delta = bin_position - self.current_bin
            try:
                if delta:
                    self.stepper_motor.motor_go(math.copysign(1, delta) > 0, "Full" , abs(2550 * delta), .0005, False, .05)
                    self.current_bin = bin_position

                    if not hold:
                        self.servo.drive(20000)
                        sleep(1)
                        self.servo.drive(60000)
                        sleep(1)

                    with open(self.file_path, "wb") as f:
                        pickle.dump(self.current_bin, f)

            except:
                pass

def test_swap():
    servo = Servo(13)
    while(True):
        servo.min()
        sleep(1)
        servo.max()
        sleep(1)

def test_hold(position):
    servo = Servo(13)
    while(True):
        servo.value = position

def test_hold2(pos):
    servo = 13

    pwm = pigpio.pi()
    pwm.set_mode(servo, pigpio.OUTPUT)
    pwm.set_PWM_frequency(servo, 50)
    
    pwm.hardware_PWM(servo, 50, pos)


if __name__ == '__main__':
   
    #GpioPins = [18, 23, 24, 25]
    #mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
    #while(1):
    #    mymotortest.motor_run(GpioPins , .001, 500, False, True, "half", .05)
    #    sleep(1)
    #GPIO.cleanup()
    #test_swap()
   
    #GPIO.cleanup()
    motor = Motor(direction_pin=17, step_pin=18, file_path="./bin_position.pkl", servo_pin=13)
    #test_hold2(60000)
    #try:
    #motor.go_to_bin(-1)
    #motor.go_to_bin(4, hold=True)
    #motor.go_to_bin(0, hold=True)
    #motor.go_to_bin(2)
    #while True:
    motor.stepper_motor.motor_go(False, "Full" , 2550, .0005, False, .05)
    motor.gate.pwm.hardware_PWM(motor.gate.servo, 50, 20000)
    sleep(1)
    motor.gate.pwm.hardware_PWM(motor.gate.servo, 50, 60000)
    #    sleep(1)
    #    motor.stepper_motor.motor_go(False, "Full" , 2550, .0005, True, .05)
    #    sleep(1)
    #motor.go_to_bin(1)
    #motor.go_to_bin(2)
    #motor.go_to_bin(3)
    #motor.go_to_bin(2)

    #while(True):
    #    sleep(1)
    pass