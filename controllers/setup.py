import customtkinter as ctk
from PIL import Image

class SetupController :
    def __init__(self, model, view, routes):
        self.model = model
        self.view = view
        self.frame = self.view.current_frame
        self._bind(routes)

        self.frame.bins = self.model.bin_state.bins
        #self.frame.enables = self.model.bin_state.enables
        self.frame.create_draggable_labels()

        #for btn in self.frame.buttons:
        #    btn.configure(command=lambda id=btn.id: self.toggle_enable(id))

        img = Image.open("./resources/exit-btn.png")
        btn_img = ctk.CTkImage(img, size=(60, 60))
        self.frame.save_btn = ctk.CTkButton(self.frame, width=60, height=60, text="", image=btn_img, fg_color="#d3f3d3", hover_color="#d3f3d3", command=self.save_bin_state)
        self.frame.save_btn.place(x=700, y=22)

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