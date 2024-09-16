class BinState:
    bins = ["normal", "wet", "bottle", "can"]
    enables = [True, True, True, True]

    def __init__(self, ir_sensors):
        super().__init__()
        self.ir_sensors = ir_sensors

    def update_bin_state(self):
        is_bin_full = [bool(sr.check()) for sr in self.ir_sensors]
        return is_bin_full
