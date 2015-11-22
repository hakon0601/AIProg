import tkinter as tk

from game_controller import GameController


class Gui(tk.Tk):
    def __init__(self, delay, collect_cases=False, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("2048-solver Neural nets")
        self.cell_width = self.cell_height = 100
        self.dim = (4, 4)
        self.delay=delay
        screen_width = self.dim[0]*self.cell_width+1
        screen_height = self.dim[1]*self.cell_height+1
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.color_dict = self.fill_color_dict()
        #self.bind_keys()

        self.controller = GameController(collect_cases=collect_cases)
        self.do_iteration()

    def do_iteration(self):
        self.controller.run_algorithm()
        self.draw_board()
        if self.controller.continuing:
            self.after(self.delay, lambda: self.do_iteration())

    def bind_keys(self):
        self.bind('<Up>', lambda event: self.move(self, self.game_board.move_up()))
        self.bind('<Down>', lambda event: self.move(self, self.game_board.move_down()))
        self.bind('<Right>', lambda event: self.move(self, self.game_board.move_right()))
        self.bind('<Left>', lambda event: self.move(self, self.game_board.move_left()))

    def move(self, event, is_moved):
        if is_moved:
            self.game_board.generate_new_node()
            self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for y in range(self.dim[1]):
                for x in range(self.dim[0]):
                    x1 = x * self.cell_width
                    y1 = self.dim[1]*self.cell_height - y * self.cell_height
                    x2 = x1 + self.cell_width
                    y2 = y1 - self.cell_height
                    cell_type = self.controller.board[y][x]
                    text = str(self.controller.board[y][x])
                    color = self.color_dict[str(self.controller.board[y][x])]
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="rect")
                    if cell_type != 0:
                        self.canvas.create_text(x1+self.cell_width/2, y1-self.cell_height/2, text=text)

    def fill_color_dict(self):
        color_dict = {
            '0': "white",
            '2': "lemon chiffon",
            '4': "peach puff",
            '8': "sandy brown",
            '16': "dark orange",
            '32': "salmon",
            '64': "tomato",
            '128': "khaki",
            '256': "khaki",
            '512': "red",
            '1024': "light goldenrod",
            '2048': "firebrick",
            '4096': "dim grey",
            '8192': "light goldenrod",
        }
        return color_dict

if __name__ == "__main__":
    app = Gui(delay=2, collect_cases=False)
    app.mainloop()
