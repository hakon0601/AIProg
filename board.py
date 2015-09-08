__author__ = 'hakon0601'

import input_handler


class Board():
    def __init__(self, filename):
        self.obstacles = []
        self.board = []
        self.dim = self.start = self.goal = (0, 0)
        self.path_len = None
        if filename:
            input_handler.read_file(self, filename)
        else:
            input_handler.prompt_user_input(self)
        self.build_board()

    def build_board(self):
        self.board = [["O" for x in range(self.dim[0])] for y in range(self.dim[1])]
        self.board[self.start[1]][self.start[0]] = "S"
        self.board[self.goal[1]][self.goal[0]] = "G"
        for obstacle in self.obstacles:
            self.place_obstacle_on_board(obstacle)


    def place_obstacle_on_board(self, obstacle):
        for y in range(obstacle[3]):
            for x in range(obstacle[2]):
                self.board[obstacle[1]+y][obstacle[0]+x] = "X"

    def print_board(self):
        for board_row in reversed(self.board):
            print([node for node in board_row])
