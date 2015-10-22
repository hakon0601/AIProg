from math import sqrt
from game2048 import Game2048
import copy
from itertools import count
import random

class State():
    _ids = count(0)

    def __init__(self, board, depth, move=None, is_max=None):
        self.id = self._ids.next()
        self.board = board
        self.depth = depth
        self.h_value = float("inf")
        self.children = []
        self.parent = None
        self.a = None
        self.b = None
        self.move = move
        self.is_max = is_max

    def generate_min_successor_nodes(self):
        #print "Generating min nodes (C)"
        successor_nodes = []
        # Generate one state for each possible generated node
        if self.board.board_has_space():
            for y in range(4):
                for x in range(4):
                    if self.board.board[y][x] == 0:
                        value = 2
                        if not random.random() >= 0.90:
                            value = 2
                        else:
                            value = 4
                        # 2 board
                        new_2_board = copy.deepcopy(self.board.board)
                        new_2_board[y][x] = value
                        child = State(board=Game2048(new_2_board), depth=self.depth-1, is_max=False)
                        child.parent = self
                        self.children.append(child)
                        successor_nodes.append(child)
                        #4 board
                        # new_4_board = copy.deepcopy(self.board.board)
                        # new_4_board[y][x] = 4
                        # child = State(board=Game2048(new_4_board), depth=self.depth-1, is_max=False)
                        # child.parent = self
                        # self.children.append(child)
                        # successor_nodes.append(child)
        return successor_nodes

    def generate_max_successor_nodes(self):
        successor_nodes = []

        # All possible moves, but remove the once that does not make a move
        board_left = copy.deepcopy(self.board)
        left_moved = board_left.move_left()
        if left_moved:
            left_state = State(board_left, self.depth-1, "left", True)
            successor_nodes.append(left_state)
            self.children.append(left_state)
            left_state.parent = self

        board_right = copy.deepcopy(self.board)
        right_moved = board_right.move_right()
        if right_moved:
            right_state = State(board_right, self.depth-1, "right", True)
            successor_nodes.append(right_state)
            self.children.append(right_state)
            right_state.parent = self

        board_up = copy.deepcopy(self.board)
        up_moved = board_up.move_up()
        if up_moved:
            up_state = State(board_up, self.depth-1, "up", True)
            successor_nodes.append(up_state)
            self.children.append(up_state)
            up_state.parent = self

        board_down = copy.deepcopy(self.board)
        down_moved = board_down.move_down()
        if down_moved:
            down_state = State(board_down, self.depth-1, "down", True)
            successor_nodes.append(down_state)
            self.children.append(down_state)
            down_state.parent = self
        return successor_nodes


    def set_h(self):
        self.h_value = int(self.board.open_cells_count()*5) + int(self.board.sort_snake())

    def __str__(self):
        return "depth: " + str(self.depth) + ", move: " + str(self.move) + ", is max: " + str(self.is_max)

    def __repr__(self):
        return self.__str__()
