import customtkinter as ctk
from time import sleep
import threading
import qrcode
import PIL

class FinishController:
    def __init__(self, model, view, routes):
        self.model = model
        self.view = view
        self.frame = self.view.current_frame
        self._bind(routes)

        self.total_points = self.model.point_table.total_points

        self.frame.lbl1 = ctk.CTkLabel(self.frame, text="คุณมีแต้มสะสมทั้งหมด", font=ctk.CTkFont(size=21), fg_color="white", text_color="black")
        self.frame.lbl1.place(x=400, y=55, anchor="center")
        self.frame.lbl2 = ctk.CTkLabel(self.frame, text=f"{self.total_points} points", font=ctk.CTkFont(size=32), fg_color="white", text_color="black")
        self.frame.lbl2.place(x=400, y=85, anchor="center")

        self.count = 30
        self.frame.countdown_lbl = ctk.CTkLabel(self.frame, text=f"{self.count} วิ", text_color="black", fg_color="white", font=ctk.CTkFont(size=42))
        self.frame.countdown_lbl.place(x=710, y=250, anchor="center")

        self.loading = threading.Thread(target=self.generate_qr_code)
        self.loading.start()

        self.countdown(self.count)

    def _bind(self, routes):
        self.exit = routes[0]

    def generate_qr_code(self):
        url = None
        while url is None:
            url = self.model.transaction.getToken("/create-transaction", 5, {'er': 'se'})
            sleep(0.5)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save("./temp/qrcode.jpg")

        img = PIL.Image.open("./temp/qrcode.jpg")
        qr_img = ctk.CTkImage(img, size=(220, 220))
        self.frame.img = ctk.CTkLabel(self.frame, text="", image=qr_img)
        self.frame.img.place(x=400, y=240, anchor="center")

    def countdown(self, count):
        if count >= 0:
            self.frame.countdown_lbl.configure(text=f"{count} วิ")
            self.view.root.after(1000, self.countdown, count - 1)
        else:
            self.exit()