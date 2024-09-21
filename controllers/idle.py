import customtkinter as ctk 
from PIL import Image
import threading
from time import sleep

class IdleController:
    def __init__(self, model, view, routes):
        self.model = model
        self.view = view
        self.frame = self.view.current_frame
        self._bind(routes)

        self.model.point_table.clear()

        self.frame.lbl = ctk.CTkLabel(self.frame, text="ทิ้งขยะลงกล่องเพื่อเริ่มต้น", text_color="#00AC00", fg_color="white", font=ctk.CTkFont(size=28))
        self.frame.lbl.place(x=400, y=400, anchor="center")

        img = Image.open("./resources/setup-btn.png")
        btn_img = ctk.CTkImage(img, size=(50, 50))
        self.frame.setup_btn = ctk.CTkButton(self.frame, width=50, height=50, text="", image=btn_img, fg_color="#f0f0f0", hover_color="#f0f0f0")
        self.frame.setup_btn.configure(command=self.setup)
        self.frame.setup_btn.place(x=727, y=406)

        #self.report_bin_status()
        #self.check()
        self.job = threading.Thread(target=self.is_widget_visible)
        self.job.start()

    def _bind(self, routes):
        self.view_wait = routes[0]
        self.setup = routes[1]

    def is_widget_visible(self):
        while True:
            x = False
            try:
                x = bool(self.view.root.winfo_viewable())
            except:
                pass
            
            if(x):
                self.view.root.after(2000, self.view_wait)

    def mockup(self):
        print("=> Okay")
        self.view_wait()

    def check(self):
        try:
            active = self.model.switch.check()
            print("Test", active)
            if not active:
                self.view_wait()
            else:
                self.view.root.after(1000, self.check)
        except:
            pass

    def report_bin_status(self):
        is_bin_full = [False]
        if any(is_bin_full):
            self.frame.lbl.configure(text="ถังขยะเต็ม ยังไม่พร้อมให้บริการขณะนี้", text_color="red")
            for i, full in enumerate(is_bin_full):
                if full:
                    self.model.transaction.sendNotify("/send-notify", [i])
            self.model.transaction.has_sent = True
        else:
            self.frame.lbl.configure(text="ทิ้งขยะลงกล่องเพื่อเริ่มต้น", text_color="#00AC00")
            self.model.transaction.has_sent = False
        
        self.view.root.after(1000, self.report_bin_status)