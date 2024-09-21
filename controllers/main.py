from .idle import IdleController
from .setup import SetupController
from .wait import WaitController
from .condition import ConditionController
from .finish import FinishController

class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model
        self.controller_classes = {
            "idle": (IdleController, [lambda: self.switch("wait"), lambda: self.switch("setup")]),
            "setup": (SetupController, [lambda: self.switch("idle")]),
            "wait": (WaitController, [lambda: self.switch("condition")]),
            "condition": (ConditionController, [lambda: self.switch("idle"), lambda: self.switch("wait"), lambda: self.switch("finish")]),
            "finish": (FinishController, [lambda: self.switch("idle")]),
        }
        self.current_controller = None

    def switch(self, name):
        self.view.switch(name)
        controller = self.controller_classes[name]
        self.current_controller = controller[0](self.model, self.view, controller[1])

    def start(self):
        self.switch("idle") 
        self.view.mainloop()
