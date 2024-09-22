import customtkinter as ctk 
from PIL import Image

class IdleView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
	
        img = Image.open("./resources/idle-bg.jpg")
        bg_img = ctk.CTkImage(img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=bg_img)
        self.bg.place(x=0, y=0)
