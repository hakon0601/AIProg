from input_handler import read_file
import Tkinter as tk

class Gui():
    def __init__(self, *args, **kwargs):
        scenario = "scenarios/scenario_test.txt"
        variable_dict = read_file(scenario)
        #for keys,values in  variable_dict.items():
            #print values

if __name__ == "__main__":
    app = Gui()
    #app.mainloop()