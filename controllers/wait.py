from time import sleep
import threading

class WaitController:
    def __init__(self, model, view, routes):
        self.model = model
        self.view = view
        self.frame = self.view.current_frame
        self._bind(routes)

        self.state = "AI Analyzing."

        self.predict = threading.Thread(target=self.mockup, daemon=True)
        self.predict.start()

        self._stop_event = threading.Event()

        self.animate_thread = threading.Thread(target=self.animation, daemon=True)
        self.animate_thread.start()


    def mockup(self):
        point = self.model.point_table.calculate([('plastic_bottles', 1.0)])
        self.model.point_table.total_points += point
        print("point =>", point)

        self._stop_event.set()

        self.view_continue()


    def animation(self):
        index = 0
        progress = 0.0
        try:
            while not self._stop_event.is_set():
                # Update the label with dots animation
                dots = '.' * (index)
                self.frame.lbl.configure(text=self.state + dots)
                index += 1
                index %= 5

                # Update the progress bar
                progress += 1/5
                if progress > 1.0:
                    progress = 0.0
                self.frame.progressbar.set(progress)

                # Sleep for a short duration before the next update
                sleep(0.5)
        except:
            pass

    def _bind(self, routes):
        self.view_continue = routes[0]

    def predict_thread(self):
        prediction = []
        prediction = self.model.camera.predict()
        print(prediction)

        point = self.model.point_table.calculate(prediction)
        self.model.point_table.total_points += point
        print("point =>", point)

        self.state = "Sorting Bin."
        self.model.motor.go_to_bin(self.model.point_table.bin)
        self.model.motor.go_to_bin(3, hold=True)

        self._stop_event.set()
        self.view_continue()