class PointTable:
    def __init__(self):
        self.clear()

    def calculate(self, prediction):
        self.prediction = prediction
        self.point = 50
        self.summary = "ขยะทั่วไป"
        self.bin = 3
        
        cls = [p[0] for p in prediction]

        if "wet waste" in cls:
            self.point = 0
            self.summary = "ขยะเปียก"
            self.bin = 4
        else:
            if "can" in cls:
                self.point = 300
                self.summary = "กระป๋อง"
                self.bin = 0
            if "plastic_bottles" in cls:
                self.point = 250
                self.summary = "ขวดพลาสติก"
                self.bin = 1
            if "Glass_Bottles" in cls:
                self.point = 200
                self.summary = "ขวดแก้ว"
                self.bin = 1
        
        return self.point
    
    def clear(self):
        self.prediction = []
        self.point = None
        self.total_points = 0
        self.summary = None
        self.bin = None