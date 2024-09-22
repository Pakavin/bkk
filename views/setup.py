import customtkinter as ctk 
from PIL import Image
import os

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

        img = Image.open("./resources/setup-bg.jpg")
        bg_img = ctk.CTkImage(img, size=(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg = ctk.CTkLabel(self, text="", image=bg_img)
        self.bg.place(x=0, y=0)

        self.labels = []
        self.positions = []
        #self.buttons = []
        
    def create_draggable_labels(self):
        for i in range(len(self.bins)):
            x, y = int((700/len(self.bins) - 143)/2 + i * 700/len(self.bins) + 50), 170

            img = Image.open(os.path.join("resources", self.bins[i] + "-bin.png"))
            bin_img = ctk.CTkImage(img, size=(143, 245))

            label = DraggableLabel(self, image=bin_img, on_drag_complete=self.on_drag_complete)
            label.name = self.bins[i]
            label.place(x=x, y=y)
            self.labels.append(label)
            self.positions.append((x, y))  # Save the original position of each label
            
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