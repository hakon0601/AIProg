__author__ = 'hakon0601'

from environment_base import BaseEnvironment


class Board(BaseEnvironment):
    def __init__(self, filename, diagonal=False):
        self.filename = filename
        self.obstacles = []
        self.board = []
        self.diagonal = diagonal
        self.read_file()
        self.build_board()

    def read_file(self):
        with open(self.filename) as f:
            content = f.readlines()

        dim = content[0][1: len(content[0]) -2].split(",")
        self.dim = (int(dim[0]), int(dim[1]))
        start_goal = content[1].strip().replace(")(", ",").replace("(", "").replace(")", "").split(",")
        self.start = (int(start_goal[0]), int(start_goal[1]))
        self.goal = (int(start_goal[2]), int(start_goal[3]))

        #Creating obstacles
        for i in range(len(content) - 2):
            obstacle_row = content[i+2][1:len(content[i+2]) - 2].split(",")
            self.obstacles.append(Obstacle(int(obstacle_row[0]), int(obstacle_row[1]), int(obstacle_row[2]), int(obstacle_row[3])))

    def build_board(self):
        self.board = [[Node(x, y, self.h(x, y)) for x in range(self.dim[0])] for y in range(self.dim[1])]
        self.board[self.start[1]][self.start[0]].set_type("S")
        self.board[self.goal[1]][self.goal[0]].set_type("G")
        for obstacle in self.obstacles:
            self.place_obstacle_on_board(obstacle, self.board)

    def place_obstacle_on_board(self, obstacle, board):
        for y in range(obstacle.height):
            for x in range(obstacle.width):
                board[obstacle.y+y][obstacle.x+x].set_type("X")

    def print_board(self):
        for board_row in reversed(self.board):
            row = []
            for x in range(len(board_row)):
                row.append(board_row[x].type)
            print(row)

    def get_start_node(self):
        return self.board[self.start[1]][self.start[0]]

    def get_goal_node(self):
        return self.board[self.goal[1]][self.goal[0]]

    def get_successor_nodes(self, node):
        successors = []
        if (node.x != 0 and self.board[node.y][node.x - 1].type != "X"):
            successors.append(self.board[node.y][node.x - 1])
        if (node.y != (self.dim[1] - 1) and self.board[node.y + 1][node.x].type != "X"):
            successors.append(self.board[node.y + 1][node.x])
        if (node.x != (self.dim[0] - 1) and self.board[node.y][node.x + 1].type != "X"):
            successors.append(self.board[node.y][node.x + 1])
        if (node.y != 0 and self.board[node.y - 1][node.x].type != "X"):
            successors.append(self.board[node.y - 1][node.x])
        if (self.diagonal):
            #TODO generate diagonal neighbours
            print("TODO diagonal get successors")
        return successors

    def h(self, x, y):
        return abs(x - self.goal[0]) + abs(y - self.goal[1])

    def dist_between(self, current_node, successor):
        return 1

    def reconstruct_path(self, end_node):
        current_node = end_node.parent
        while current_node.parent:
            self.board[current_node.y][current_node.x].set_type("A")
            current_node = current_node.parent

class Obstacle():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Node():
    def __init__(self, x, y, h_value):
        self.x = x
        self.y = y
        self.type = 'O'
        self.parent = None
        self.h_value = h_value
        self.g_value = float("inf")
        self.f_value = float("inf")

    def set_type(self, type):
        self.type = type

    def set_parent(self, parent):
        self.parent = parent

    def set_g(self, g_value):
        self.g_value = g_value

    def set_f(self, f_value):
        self.f_value = f_value

    def get_f(self):
        return self.f_value