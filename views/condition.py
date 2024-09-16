import customtkinter as ctk 
from PIL import Image

class ConditionView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        img = Image.open("./resources/condition-bg.jpg")
        bg_img = ctk.CTkImage(img, size=(800, 480))
        self.bg = ctk.CTkLabel(self, text="", image=bg_img)
        self.bg.place(x=0, y=0)

        self.btn = ctk.CTkButton(self, width=380, height=55, text="ทิ้งเสร็จแล้ว", fg_color="#006600", hover_color="#00AC00", font=ctk.CTkFont(size=24))
        self.btn.place(x=400, y=370, anchor="center")
