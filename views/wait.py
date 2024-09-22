import customtkinter as ctk
from time import sleep
import threading
from PIL import Image

class WaitView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        img = Image.open("./resources/wait-bg.jpg")
        bg_img = ctk.CTkImage(img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=bg_img)
        self.bg.place(x=0, y=0)

        self.progressbar = ctk.CTkProgressBar(self, width=400, height=18, progress_color="#00AC00", fg_color="white", bg_color="#EBF9EB", orientation="horizontal")
        self.progressbar.place(x=400, y=305, anchor="center")
        self.progressbar.set(0)
	
        self.lbl = ctk.CTkLabel(self, text="AI Analyzing.", text_color="black", fg_color="#EFFAEF", font=ctk.CTkFont(size=18))
        self.lbl.place(x=400, y=335, anchor="center")
