from model import Model
from view import View
from controller import Controller


def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()

if __name__ == "__main__":
    main()
