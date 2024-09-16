import customtkinter as ctk 

class ConditionController:
    def __init__(self, model, view, routes):
        self.model = model
        self.view = view
        self.frame = self.view.current_frame
        self._bind(routes)

        category = self.model.point_table.summary
        point = self.model.point_table.point

        self.frame.lbl1 = ctk.CTkLabel(self.frame, text=f"คุณทิ้ง {category}", font=ctk.CTkFont(size=24), fg_color="white", text_color="blue")
        self.frame.lbl1.place(x=400, y=180, anchor="center")
        self.frame.lbl2 = ctk.CTkLabel(self.frame, text=f"ได้รับ {point} Point", font=ctk.CTkFont(size=36), fg_color="white", text_color="black",)
        self.frame.lbl2.place(x=400, y=225, anchor="center")

        self.count = 15
        self.frame.countdown_lbl = ctk.CTkLabel(self.frame, text=f"{self.count} วิ", text_color="black", fg_color="white", font=ctk.CTkFont(size=42))
        self.frame.countdown_lbl.place(x=710, y=250, anchor="center")

        self.check()
        self.countdown(self.count)

    def _bind(self, routes):
        self.exit = routes[0]
        self.resume = routes[1]
        self.frame.btn.configure(command=routes[2])
    
    def check(self):
        try:
            active = self.model.switch.check()
            if not active:
                self.resume()
            else:
                self.view.root.after(100, self.check)
        except:
            pass

    def countdown(self, count):
        try:
            if count >= 0:
                self.frame.countdown_lbl.configure(text=f"{count} วิ")
                self.view.root.after(1000, self.countdown, count - 1)
            else:
                self.exit()
        except:
            pass