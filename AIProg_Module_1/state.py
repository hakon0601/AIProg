from math import sqrt

import state_base


class State(state_base.BaseState):
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.parents = []
        self.board = board
        self.h_value = float("inf")
        self.g_value = float("inf")
        self.children = []

    def get_f(self):
        return self.g_value + self.h_value

    def getID(self):
        return self.__hash__()

    def __hash__(self):
        return hash((self.x, self.y))

    # Manhattan distance
    def calculate_h(self):
        goal_x = self.board.goal[0]
        goal_y = self.board.goal[1]
        if self.board.diagonal:
            return sqrt(pow(self.x - goal_x, 2) + pow(self.y - goal_y, 2))
        return abs(self.x - goal_x) + abs(self.y - goal_y)

    def reconstruct_path(self):
        path = [self]
        while path[-1].parents:
            path.append(path[-1].get_best_parent())
        return list(reversed(path))

    def generate_successor_nodes(self):
        successors = []
        # W, NW, N, NE, E, SE, S, SW
        # Check if obstacle or outside board (if they are, the states are not generated)
        if self.x != 0 and self.board.board[self.y][self.x - 1] != "X":
            successors.append(State(self.x - 1, self.y, self.board))
        if self.board.diagonal and self.x != 0 and self.y != (self.board.dim[1] - 1) and self.board.board[self.y + 1][self.x -1] != "X":
            successors.append(State(self.x - 1, self.y + 1, self.board))
        if self.y != (self.board.dim[1] - 1) and self.board.board[self.y + 1][self.x] != "X":
            successors.append(State(self.x, self.y + 1, self.board))
        if self.board.diagonal and self.x != (self.board.dim[0] - 1) and self.y != (self.board.dim[1] - 1) and self.board.board[self.y + 1][self.x + 1] != "X":
            successors.append(State(self.x + 1, self.y + 1, self.board))
        if self.x != (self.board.dim[0] - 1) and self.board.board[self.y][self.x + 1] != "X":
            successors.append(State(self.x + 1, self.y, self.board))
        if self.board.diagonal and self.x != (self.board.dim[0] - 1) and self.y != 0 and self.board.board[self.y - 1][self.x + 1] != "X":
            successors.append(State(self.x + 1, self.y - 1, self.board))
        if self.y != 0 and self.board.board[self.y - 1][self.x] != "X":
            successors.append(State(self.x, self.y - 1, self.board))
        if self.board.diagonal and self.x != 0 and self.y != 0 and self.board.board[self.y - 1][self.x - 1] != "X":
            successors.append(State(self.x - 1, self.y - 1, self.board))
        return successors

    # Euclidian distance
    # Used to return movement cost from this state to another
    def movement_cost(self, successor):
        return sqrt(abs(self.x - successor.x) + abs(self.y - successor.y))

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.get_f() < other.get_f():
            return True
        elif self.get_f() > other.get_f():
            return False
        else:
            if self.h_value <= other.h_value:
                return True
            else:
                return False

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ") - f: " + str(self.get_f()) + " , h: " + str(self.h_value)

    def __repr__(self):
        return self.__str__()

    def get_best_parent(self):
        best_parent = self.parents[0]
        for parent in self.parents:
            if parent.g_value + parent.movement_cost(self) < best_parent.g_value + best_parent.movement_cost(self):
                best_parent = parent
        return best_parent
