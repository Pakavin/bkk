import customtkinter as ctk 
from PIL import Image
import threading
from time import sleep

from model import Model
from view import View


x = 2.4
y = 2.25


class IdleController:
    def __init__(self, model, view, routes) -> None:
        self.model = model
        self.view = view
        self.current_name = self.view.current_name
        self.frame = self.view.frames[self.view.current_name]
        self._bind(routes)

        self.model.table.clear()
        
        self.frame.setup_btn.configure(command=self.setup)

        #self.report_bin_status()
        #self.check()
        #self.listener = threading.Thread(target=self.is_widget_visible)
        #self.listener.start()

        self.report_bin_status()

    def _bind(self, routes):
        self.view_wait = routes[0]
        self.setup = routes[1]

    def is_widget_visible(self):
        while True:
            visible = False
            try:
                visible = bool(self.view.winfo_viewable())
            except:
                pass   
            if(visible):
                sleep(5)
                if(self.current_name == self.view.current_name): 
                    self.view_wait()
                else:
                    break

    def report_bin_status(self):
        is_bin_full = self.model.bin_state.update_bin_state()
        
        if any(is_bin_full):
            print(is_bin_full)

            self.frame.lbl.configure(text="ถังขยะเต็ม ยังไม่พร้อมให้บริการขณะนี้", text_color="red")
            for i, full in enumerate(is_bin_full):
                if full:
                    print(i)
                    self.model.transaction.sendNotify("/send-notify", [i])
            self.model.transaction.has_sent = True
        else:
            self.frame.lbl.configure(text="ทิ้งขยะลงกล่องเพื่อเริ่มต้น", text_color="#00AC00")
            self.model.transaction.has_sent = False

        if self.current_name == self.view.current_name:
            self.view.after(1000, self.report_bin_status)


class SetupController:
    def __init__(self, model, view, routes):
        self.model = model
        self.view = view
        self.current_name = self.view.current_name
        self.frame = self.view.frames[self.view.current_name]
        self._bind(routes)

        self.frame.bins = self.model.bin_state.bins
        #self.frame.enables = self.model.bin_state.enables
        self.frame.create_draggable_labels()

        #for btn in self.frame.buttons:
        #    btn.configure(command=lambda id=btn.id: self.toggle_enable(id))

        self.frame.save_btn.configure(command=self.save_bin_state)

    def _bind(self, routes):
        self.exit = routes[0]

    def toggle_enable(self, id):
        btn = self.frame.buttons[id]
        btn.enable = not btn.enable
        if btn.enable:
            btn.configure(text="Enable", fg_color="#006600", hover_color="#006600")
        else:
            btn.configure(text="Disable", fg_color="#545454", hover_color="#545454")

    def save_bin_state(self):
        self.model.bin_state.bins = [bin.name for bin in self.frame.labels]
        #self.model.bin_state.enables = [bin.enable for bin in self.frame.buttons]

        print(self.model.bin_state.bins)
        #print(self.model.bin_state.enables)

        self.exit()


class WaitController:
    def __init__(self, model, view, routes) -> None:
        self.model = model
        self.view = view
        self.current_name = self.view.current_name
        self.frame = self.view.frames[self.view.current_name]
        self._bind(routes)

        self.state = "AI Analyzing."

        self.animate_thread = threading.Thread(target=self.animation)
        self.animate_thread.start()

        self.loading = threading.Thread(target=self.detect)
        self.loading.start()

    def _bind(self, routes):
        self.view_continue = routes[0]

    def detect(self):
        prediction = self.model.camera.detect()

        point = self.model.table.calculate(prediction)
        self.model.table.total_points += point
        print("point =>", point)

        self.model.motor.go_to_bin(self.model.bin_state.index(self.model.table.bin))

        self.view_continue()

    def animation(self):
            index = 0
            progress = 0.0
            try:
                while self.current_name == self.view.current_name:
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


class ConditionController:
    def __init__(self, model, view, routes) -> None:
        self.model = model
        self.view = view
        self.current_name = self.view.current_name
        self.frame = self.view.frames[self.view.current_name]
        self._bind(routes)

        self.category = self.model.table.summary
        self.point = self.model.table.point
     
        self.frame.lbl1.configure(text=f"คุณทิ้ง {self.category}")
        self.frame.lbl2.configure(text=f"ได้รับ {self.point} Point")

        self.count = 15
        self.frame.countdown_lbl.configure(text=f"{self.count} วิ")

        self.countdown(self.count)

    def _bind(self, routes):
        self.exit = routes[0]
        self.resume = routes[1]
        self.frame.btn.configure(command=routes[2])
    
    def countdown(self, count):
        try:
            if self.current_name == self.view.current_name:
                if count >= 0:
                    self.frame.countdown_lbl.configure(text=f"{count} วิ")
                    self.view.after(1000, self.countdown, count - 1)
                else:
                    self.exit()
        except:
            pass


class FinishController:
    import qrcode 

    def __init__(self, model, view, routes) -> None:
        self.model = model
        self.view = view
        self.current_name = self.view.current_name
        self.frame = self.view.frames[self.view.current_name]
        self._bind(routes)

        self.total_points = self.model.table.total_points

        self.frame.lbl2.configure(text=f"{self.total_points} points")

        self.count = 30
        self.frame.countdown_lbl.configure(text=f"{self.count} วิ")

        self.loading = threading.Thread(target=self.generate_qr_code)
        self.loading.start()

        self.countdown(self.count)

    
    def _bind(self, routes):
        self.exit = routes[0]

    def generate_qr_code(self):
        url = None
        while url is None:
            url = self.model.transaction.getToken("/create-transaction", self.total_points, {'er': 'se'})
            sleep(0.5)

        qr = self.qrcode.QRCode(
            version=1,
            error_correction=self.qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save("./temp/qrcode.jpg")

        img = Image.open("./temp/qrcode.jpg")
        qr_img = ctk.CTkImage(img, size=(int(220*x), int(220*x)))
        self.frame.img = ctk.CTkLabel(self.frame, text="", image=qr_img)
        self.frame.img.place(x=int(400*x), y=int(240*y), anchor="center")

    def countdown(self, count):
        if self.current_name == self.view.current_name:
            if count >= 0:
                self.frame.countdown_lbl.configure(text=f"{count} วิ")
                self.view.after(1000, self.countdown, count - 1)
            else:
                self.exit()


class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model
        self.controllers = {
            "idle": (IdleController, [lambda: self.switch("wait"), lambda: self.switch("setup")]),
            "setup": (SetupController, [lambda: self.switch("idle")]),
            "wait": (WaitController, [lambda: self.switch("condition")]),
            "condition": (ConditionController, [lambda: self.switch("idle"), lambda: self.switch("wait"), lambda: self.switch("finish")]),
            "finish": (FinishController, [lambda: self.switch("idle")]),
        }
        self.current_controller = None


    def switch(self, new_name):
        if self.current_controller is not None:
            del self.current_controller

        self.view.switch(new_name)

        controller = self.controllers[new_name]
        self.current_controller = controller[0](self.model, self.view, controller[1])

    def start(self):
        self.switch("idle") 
        self.view.mainloop()

if __name__ == '__main__':
    ctrl = Controller(Model(), View())
    ctrl.start()