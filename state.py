from math import sqrt

class State():
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.parent = None
        self.board = board
        self.h_value = self.calculate_h(x, y, board.goal[0], board.goal[1])
        self.g_value = float("inf")

    def get_f(self):
        return self.g_value + self.h_value

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    # Manhattan distance
    def calculate_h(self, x, y, goal_x, goal_y):
        return abs(x - goal_x) + abs(y - goal_y)

    def reconstruct_path(self):
        path = [self]
        while path[-1].parent:
            path.append(path[-1].parent)
        return list(reversed(path))

    def generate_successor_nodes(self):
        successors = []
        # W, N, E, S
        # Check if obstacle or outside board (if they are, the states are not generated)
        if self.x != 0 and self.board.board[self.y][self.x - 1] != "X":
            successors.append(State(self.x - 1, self.y, self.board))
        if self.y != (self.board.dim[1] - 1) and self.board.board[self.y + 1][self.x] != "X":
            successors.append(State(self.x, self.y + 1, self.board))
        if self.x != (self.board.dim[0] - 1) and self.board.board[self.y][self.x + 1] != "X":
            successors.append(State(self.x + 1, self.y, self.board))
        if self.y != 0 and self.board.board[self.y - 1][self.x] != "X":
            successors.append(State(self.x, self.y - 1, self.board))
       # TODO
        '''
        if self.diagonal:
            # NW, NE, SE, SW
            if self.x != 0 and self.y != 0 and self.board[self.y - 1][self.x - 1].type != "X":
                successors.append(self.board[self.y - 1][self.x - 1])
            if self.x != (self.dim[0] - 1) and self.y != 0 and self.board[self.y - 1][self.x + 1].type != "X":
                successors.append(self.board[self.y - 1][self.x + 1])
            if self.x != (self.dim[0] - 1) and self.y != (self.dim[1] - 1) and self.board[self.y + 1][self.x + 1].type != "X":
                successors.append(self.board[self.y + 1][self.x + 1])
            if self.x != 0 and self.y != (self.dim[1] - 1) and self.board[self.y + 1][self.x -1].type != "X":
                successors.append(self.board[self.y + 1][self.x - 1])
        '''
        return successors

    # Euclidian distance
    # Used to return movement cost from one node to another
    def movement_cost(self, successor):
        return sqrt(abs(self.x - successor.x) + abs(self.y - successor.y))

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

'''
Type O is free node
Type X is obstacle node
Type G is goal node
Type S is start node
'''

'''



'''
