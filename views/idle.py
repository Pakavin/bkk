import customtkinter as ctk 
from PIL import Image

class IdleView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
	
        img = Image.open("./resources/idle-bg.jpg")
        bg_img = ctk.CTkImage(img, size=(800, 480))
        self.bg = ctk.CTkLabel(self, text="", image=bg_img)
        self.bg.place(x=0, y=0)
