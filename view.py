import customtkinter as ctk 
from time import sleep
from PIL import Image
import os

x = 2.4
y = 2.25

class IdleView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
	
        self.img = Image.open("./resources/idle-bg.jpg")
        self.bg_img = ctk.CTkImage(self.img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=self.bg_img)
        self.bg.place(x=0, y=0)
        
        self.lbl = ctk.CTkLabel(self, text="ทิ้งขยะลงกล่องเพื่อเริ่มต้น", text_color="#00AC00", fg_color="white", font=ctk.CTkFont(size=int(28*x)))
        self.lbl.place(x=int(400*x), y=int(400*y), anchor="center")

        img = Image.open("./resources/setup-btn.png")
        btn_img = ctk.CTkImage(img, size=(int(50*x), int(50*y)))
        self.setup_btn = ctk.CTkButton(self, width=int(50*x), height=int(50*y), text="", image=btn_img, fg_color="#f0f0f0", hover_color="#f0f0f0")
        self.setup_btn.place(x=int(727*x), y=int(406*y))



class DraggableLabel(ctk.CTkLabel):
    def __init__(self, parent, image, on_drag_complete, *args, **kwargs):
        super().__init__(parent, text="", image=image, *args, **kwargs)
        self.on_drag_complete = on_drag_complete
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.dragging = False
        self.start_x = 0
        self.start_y = 0
        self.original_pos = (0, 0)  # To store original position

    def start_drag(self, event):
        self.dragging = True
        self.start_x = event.x
        self.start_y = event.y
        self.original_pos = (self.winfo_x(), self.winfo_y())

    def do_drag(self, event):
        if self.dragging:
            x = self.winfo_x() + event.x - self.start_x
            y = self.winfo_y() + event.y - self.start_y
            self.place(x=x, y=y)

    def stop_drag(self, event):
        if self.dragging:
            self.dragging = False
            self.on_drag_complete(self)


class SetupView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
	
        self.img = Image.open("./resources/setup-bg.jpg")
        self.bg_img = ctk.CTkImage(self.img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=self.bg_img)
        self.bg.place(x=0, y=0)

        self.labels = []
        self.positions = []
        #self.buttons = []

        
        img = Image.open("./resources/exit-btn.png")
        btn_img = ctk.CTkImage(img, size=(int(60*x), int(60*y)))
        self.save_btn = ctk.CTkButton(self, width=int(60*x), height=int(60*y), text="", image=btn_img, fg_color="#d3f3d3", hover_color="#d3f3d3")
        self.save_btn.place(x=int(700*x), y=int(22*y))

        
    def create_draggable_labels(self):
        for i in range(len(self.bins)):
            x_, y_ = int((700/len(self.bins) - 143)/2 + i * 700/len(self.bins) + 50), 170
            x_, y_ = int(x_*x), int(y_*y)

            img = Image.open(os.path.join("resources", self.bins[i] + "-bin.png"))
            bin_img = ctk.CTkImage(img, size=(int(143*x), int(245*y)))

            label = DraggableLabel(self, image=bin_img, on_drag_complete=self.on_drag_complete)
            label.name = self.bins[i]
            label.place(x=x_, y=y_)
            self.labels.append(label)
            self.positions.append((x_, y_))  # Save the original position of each label
            
            #button = ctk.CTkButton(self, width=143,  height=24, font=ctk.CTkFont(size=24))
            #button.id = i
            #button.enable = self.enables[i]
            #if button.enable:
            #    button.configure(text="Enable", fg_color="#006600", hover_color="#006600")
            #else:
            #    button.configure(text="Disable", fg_color="#545454", hover_color="#545454")

            #button.place(x=x, y=410)
            #self.buttons.append(button)

    def on_drag_complete(self, dragged_label):
        # Find the closest available position from predefined positions
        closest_position = self.find_closest_position(dragged_label)
        idx = self.positions.index(closest_position)

        # Reorder the labels list based on dragging
        self.labels.remove(dragged_label)
        self.labels.insert(idx, dragged_label)

        # Snap dragged label to the closest position and update the positions of all labels
        self.reorganize_labels()

    def find_closest_position(self, dragged_label):
        # Get the current position of the dragged label
        dragged_x, dragged_y = dragged_label.winfo_x(), dragged_label.winfo_y()

        # Find the closest position from the predefined positions
        closest_pos = min(self.positions, key=lambda pos: (pos[0] - dragged_x) ** 2 + (pos[1] - dragged_y) ** 2)
        return closest_pos

    def reorganize_labels(self):
        # Reorganize all labels to snap them to their nearest positions
        for i, lbl in enumerate(self.labels):
            lbl.place(x=self.positions[i][0], y=self.positions[i][1])


class WaitView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
	
        self.img = Image.open("./resources/wait-bg.jpg")
        self.bg_img = ctk.CTkImage(self.img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=self.bg_img)
        self.bg.place(x=0, y=0)
        
        self.progressbar = ctk.CTkProgressBar(self, width=int(400*x), height=int(18*y), progress_color="#00AC00", fg_color="white", bg_color="#EBF9EB", orientation="horizontal")
        self.progressbar.place(x=int(400*x), y=int(305*y), anchor="center")
        self.progressbar.set(0)
	
        self.lbl = ctk.CTkLabel(self, text="AI Analyzing.", text_color="black", fg_color="#EFFAEF", font=ctk.CTkFont(size=int(18*x)))
        self.lbl.place(x=int(400*x), y=int(335*y), anchor="center")


class ConditionView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.img = Image.open("./resources/condition-bg.jpg")
        self.bg_img = ctk.CTkImage(self.img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=self.bg_img)
        self.bg.place(x=0, y=0)

        self.btn = ctk.CTkButton(self, width=int(380*x), height=int(55*y), text="ทิ้งเสร็จแล้ว", fg_color="#006600", hover_color="#00AC00", font=ctk.CTkFont(size=int(24*x)))
        self.btn.place(x=int(400*x), y=int(370*y), anchor="center")

        self.lbl1 = ctk.CTkLabel(self, font=ctk.CTkFont(size=int(24*x)), fg_color="white", text_color="blue")
        self.lbl1.place(x=int(400*x), y=int(180*y), anchor="center")
        self.lbl2 = ctk.CTkLabel(self, font=ctk.CTkFont(size=int(36*x)), fg_color="white", text_color="black",)
        self.lbl2.place(x=int(400*x), y=int(225*y), anchor="center")

        self.countdown_lbl = ctk.CTkLabel(self, text_color="black", fg_color="white", font=ctk.CTkFont(size=int(42*x)))
        self.countdown_lbl.place(x=int(710*x), y=int(250*y), anchor="center")


class FinishView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
	
        self.img = Image.open("./resources/finish-bg.jpg")
        self.bg_img = ctk.CTkImage(self.img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=self.bg_img)
        self.bg.place(x=0, y=0)

        self.lbl1 = ctk.CTkLabel(self, text="คุณมีแต้มสะสมทั้งหมด", font=ctk.CTkFont(size=int(21*x)), fg_color="white", text_color="black")
        self.lbl1.place(x=int(400*x), y=int(55*y), anchor="center")
        self.lbl2 = ctk.CTkLabel(self, font=ctk.CTkFont(size=32), fg_color="white", text_color="black")
        self.lbl2.place(x=int(400*x), y=int(85*y), anchor="center")

        self.countdown_lbl = ctk.CTkLabel(self, text_color="black", fg_color="white", font=ctk.CTkFont(size=int(42*x)))
        self.countdown_lbl.place(x=int(710*x), y=int(250*y), anchor="center")


class View(ctk.CTk):
    def __init__(self, debug=True):
        super().__init__()

        ctk.set_appearance_mode("white")
        self.config(cursor="none")

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.attributes('-topmost', True)

        print(self.winfo_screenwidth() / 800, self.winfo_screenheight() / 480)
    
        self.frames = {
            "idle": IdleView(self),
            "setup": SetupView(self),
            "wait": WaitView(self),
	        "condition": ConditionView(self),
            "finish": FinishView(self)
        }

        if not debug:
            self.overrideredirect(True)

        self.current_name = None

        #self.after(3000, lambda: self.switch("wait"))
        #self.after(6000, lambda: self.switch("condition"))
        #self.after(9000, lambda: self.switch("finish"))


    def switch(self, new_name):
        if self.current_name is not None:
            self.frames[self.current_name].pack_forget()
        
        self.frames[new_name].pack(expand=True, fill="both")
        self.current_name = new_name


if __name__ == '__main__':
    app = View(debug=False)
    app.switch("wait")
    app.mainloop()