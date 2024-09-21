from .sensor import *
from .binstate import BinState
from .transaction import Transaction
from .motor import Motor
from .camera import Camera
from .point import PointTable

class Model:
    def __init__(self):
        self.switch = MagneticSwitch(26)
        self.bin_state = BinState([IRSensor(5, 60), IRSensor(8, 60)])
        #self.motor = Motor(direction_pin=17, step_pin=18, file_path="./temp/bin_position.pkl", gate=Gate(13))
        self.transaction = Transaction("https://apibkkbinplus.vercel.app")
        #self.camera = Camera(["./resources/dry waste-wet waste.pt", "./resources/Glass_Bottles-can-plastic_bottles.pt"])
        self.point_table = PointTable()