from .root import Root
from .idle import IdleView
from .setup import SetupView
from .wait import WaitView
from .condition import ConditionView
from .finish import FinishView

class View:
    def __init__(self):
        self.root = Root()
        self.frame_classes = {
            "idle": IdleView,
            "setup": SetupView,
            "wait": WaitView,
	        "condition": ConditionView,
            "finish": FinishView
        }
        self.current_frame = None

    def switch(self, name):
        new_frame = self.frame_classes[name](self.root)

        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        

    def mainloop(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = View()
    app.mainloop()
