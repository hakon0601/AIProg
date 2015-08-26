__author__ = 'hakon0601'

from environment_base import BaseEnvironment
from math import sqrt
from node import Node
import input_handler


class Board(BaseEnvironment):
    def __init__(self, filename, diagonal=False):
        self.obstacles = []
        self.board = []
        self.dim = self.start = self.goal = (0, 0)
        self.path_len = None
        self.diagonal = diagonal
        if filename:
            input_handler.read_file(self, filename)
        else:
            input_handler.prompt_user_input(self)
        self.build_board()

    def build_board(self):
        self.board = [[Node(x, y, self.h(x, y)) for x in range(self.dim[0])] for y in range(self.dim[1])]
        self.get_start_node().type = "S"
        self.get_goal_node().type = "G"
        for obstacle in self.obstacles:
            self.place_obstacle_on_board(obstacle, self.board)

    def place_obstacle_on_board(self, obstacle, board):
        for y in range(obstacle.height):
            for x in range(obstacle.width):
                board[obstacle.y+y][obstacle.x+x].type = "X"

    def print_board(self):
        for board_row in reversed(self.board):
            print([node.type for node in board_row])

    def get_start_node(self):
        return self.board[self.start[1]][self.start[0]]

    def get_goal_node(self):
        return self.board[self.goal[1]][self.goal[0]]

    def get_successor_nodes(self, node):
        successors = []
        # W, N, E, S
        if node.x != 0 and self.board[node.y][node.x - 1].type != "X":
            successors.append(self.board[node.y][node.x - 1])
        if node.y != (self.dim[1] - 1) and self.board[node.y + 1][node.x].type != "X":
            successors.append(self.board[node.y + 1][node.x])
        if node.x != (self.dim[0] - 1) and self.board[node.y][node.x + 1].type != "X":
            successors.append(self.board[node.y][node.x + 1])
        if node.y != 0 and self.board[node.y - 1][node.x].type != "X":
            successors.append(self.board[node.y - 1][node.x])
        if self.diagonal:
            # NW, NE, SE, SW
            if node.x != 0 and node.y != 0 and self.board[node.y - 1][node.x - 1].type != "X":
                successors.append(self.board[node.y - 1][node.x - 1])
            if node.x != (self.dim[0] - 1) and node.y != 0 and self.board[node.y - 1][node.x + 1].type != "X":
                successors.append(self.board[node.y - 1][node.x + 1])
            if node.x != (self.dim[0] - 1) and node.y != (self.dim[1] - 1) and self.board[node.y + 1][node.x + 1].type != "X":
                successors.append(self.board[node.y + 1][node.x + 1])
            if node.x != 0 and node.y != (self.dim[1] - 1) and self.board[node.y + 1][node.x -1].type != "X":
                successors.append(self.board[node.y + 1][node.x - 1])

        return successors

    # Manhattan distance
    def h(self, x, y):
        return abs(x - self.goal[0]) + abs(y - self.goal[1])

    # Euclidian distance
    # Used to return movement cost from one node to another
    def movement_cost(self, current_node, successor):
        return sqrt(abs(current_node.x - successor.x) + abs(current_node.y - successor.y))

    @staticmethod
    def reconstruct_path(end_node):
        path = [end_node]
        while path[-1].parent:
            path.append(path[-1].parent)
        return list(reversed(path))
