from input_handler import read_file
import Tkinter as tk

class Gui():
    def __init__(self, *args, **kwargs):
        scenario = "scenarios/scenario_test.txt"
        read_file(scenario)

if __name__ == "__main__":
    app = Gui()
    #app.mainloop()