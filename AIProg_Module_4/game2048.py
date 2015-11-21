import random
import copy
import itertools

class Game2048():
    def __init__(self, board=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]):
        self.board = board

    def is_game_over(self):
        if self.can_move() == False and self.board_has_space() == False:
            return True
        return False

    def move_left(self):
            is_calculated = is_moved = False
            for y in range(4):
                for x in range(1,4):
                    this_place = self.board[y][x]
                    if this_place != 0:
                        one_back = self.board[y][x-1]
                        two_back = self.board[y][x-2]
                        three_back = self.board[y][x-3]
                        if x-1 >= 0 and this_place == one_back:
                            self.board[y][x-1] = one_back*2
                            self.board[y][x] = 0
                            is_calculated = True
                        elif x-2 >= 0 and this_place == two_back and one_back == 0:
                            self.board[y][x-2] = two_back*2
                            self.board[y][x] = 0
                            is_calculated = True
                        elif x-3 >= 0 and this_place == three_back and one_back == 0 and two_back == 0:
                            self.board[y][x-3] = three_back*2
                            self.board[y][x] = 0
                            is_calculated = True
                        if this_place != 0:
                            if self.move_horisontal(y=y, x=x, x1=x-1, x2=x-2, x3=x-3, max1=x-1>=0, max2=x-2>=0, max3=x-3>=0):
                                is_moved = True
            return is_calculated or is_moved

    def move_right(self):
        if self.can_move() == False and self.board_has_space() == False:
            self.game_over = True
        is_calculated = is_moved = False
        for y in range(4):
            for x in range(2,-1,-1):
                this_place = self.board[y][x]
                if this_place != 0:
                    if x+1 <= 3 and this_place == self.board[y][x+1]:
                        self.board[y][x+1] = self.board[y][x+1]*2
                        self.board[y][x] = 0
                        is_calculated = True
                    elif x+2 <= 3 and this_place == self.board[y][x+2] and self.board[y][x+1] == 0:
                        self.board[y][x+2] = self.board[y][x+2]*2
                        self.board[y][x] = 0
                        is_calculated = True
                    elif x+3 <= 3 and this_place == self.board[y][x+3] and self.board[y][x+1] == 0 and self.board[y][x+2] == 0:
                        self.board[y][x+3] = self.board[y][x+3]*2
                        self.board[y][x] = 0
                        is_calculated = True
                    if self.move_horisontal(y=y, x=x, x1=x+1, x2=x+2, x3=x+3, max1=x+1 <= 3, max2=x+2 <= 3, max3=x+3 <= 3):
                        is_moved = True
        return is_calculated or is_moved

    def move_up(self):
        if self.can_move() == False and self.board_has_space() == False:
            self.game_over = True
        is_calculated = is_moved = False
        for x in range(4):
            for y in range(2,-1,-1):
                this_place = self.board[y][x]
                if this_place != 0:
                    if y+1 <= 3 and this_place == self.board[y+1][x]:
                        self.board[y+1][x] = self.board[y+1][x]*2
                        self.board[y][x] = 0
                        is_calculated = True
                    elif y+2 <= 3 and this_place == self.board[y+2][x] and self.board[y+1][x] == 0:
                        self.board[y+2][x] = self.board[y+2][x]*2
                        self.board[y][x] = 0
                        is_calculated = True
                    elif y+3 <= 3 and this_place == self.board[y+3][x] and self.board[y+3][x] == 0 and self.board[y+2][x] == 0:
                        self.board[y+3][x] = self.board[y+3][x]*2
                        self.board[y][x] = 0
                        is_calculated = True
                    if this_place != 0:
                        if self.move_vertical(y=y, x=x, y1=y+1, y2=y+2, y3=y+3, max1=y+1 <= 3, max2=y+2 <= 3, max3=y+3 <= 3):
                            is_moved = True
        return is_moved or is_calculated

    def move_down(self):
        if self.can_move() == False and self.board_has_space() == False:
            self.game_over = True
        is_calculated = is_moved = False
        for x in range(4):
            for y in range(1,4):
                this_place = self.board[y][x]
                if this_place != 0:
                    one_back = self.board[y-1][x]
                    two_back = self.board[y-2][x]
                    three_back = self.board[y-3][x]
                    if y-1 >= 0 and this_place == one_back:
                        self.board[y-1][x] = one_back*2
                        self.board[y][x] = 0
                        is_calculated = True
                    elif y-2 >= 0 and this_place == two_back and one_back == 0:
                        self.board[y-2][x] = two_back*2
                        self.board[y][x] = 0
                        is_calculated = True
                    elif y-3 >= 0 and this_place == three_back and one_back == 0 and two_back == 0:
                        self.board[y-3][x] = three_back*2
                        self.board[y][x] = 0
                        is_calculated = True
                    if self.move_vertical(y=y, x=x, y1=y-1, y2=y-2, y3=y-3, max1=y-1 >= 0, max2=y-2 >= 0, max3=y-3 >= 0):
                        is_moved = True
    # if is_calculated or is_moved:
    #         self.generate_new_node()
        return is_moved or is_calculated

    def move_horisontal(self, y, x, x1, x2, x3, max1, max2, max3):
        is_moved = False
        if max3 and self.board[y][x3] == 0 and self.board[y][x2] == 0 and self.board[y][x1] == 0:
            self.board[y][x3] = self.board[y][x]
            self.board[y][x] = 0
            is_moved = True
        elif max2 and self.board[y][x2] == 0 and self.board[y][x1] == 0:
            self.board[y][x2] = self.board[y][x]
            self.board[y][x] = 0
            is_moved = True
        elif max1 and self.board[y][x1] == 0:
            self.board[y][x1] = self.board[y][x]
            self.board[y][x] = 0
            is_moved = True
        return is_moved

    def move_vertical(self, y, x, y1, y2, y3, max1, max2, max3):
        is_moved = False
        if max3 and self.board[y3][x] == 0 and self.board[y2][x] == 0 and self.board[y1][x] == 0:
            self.board[y3][x] = self.board[y][x]
            self.board[y][x] = 0
            is_moved = True
        elif max2 and self.board[y2][x] == 0 and self.board[y1][x] == 0:
            self.board[y2][x] = self.board[y][x]
            self.board[y][x] = 0
            is_moved = True
        elif max1 and self.board[y1][x] == 0:
            self.board[y1][x] = self.board[y][x]
            self.board[y][x] = 0
            is_moved = True
        return is_moved

    def generate_new_node(self):
        if self.board_has_space():
            if not random.random() >= 0.90:
                value = 2
            else:
                value = 4
            while True:
                self.start_x = random.randint(0,3)
                self.start_y = random.randint(0,3)
                if self.board[self.start_y][self.start_x] == 0:
                    self.board[self.start_y][self.start_x] = value
                    return
        return

    def board_has_space(self):
        is_space = False
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    is_space = True
                    break
        return is_space

    def can_move(self):
        for y in range(4):
            for x in range(4):
                # Check rows
                if x+1 <= 3:
                    if self.board[y][x] == self.board[y][x+1]:
                        return True
                # Check columns
                if y+1 <= 3:
                    if self.board[y][x] == self.board[y+1][x]:
                        return True
        return False

    def get_largest_tile(self):
        largest = 0
        for y in range(4):
            for x in range(4):
                largest = max(largest, self.board[y][x])
        return largest

############################################################################################

    def open_cells_count(self):
        open_cells = 0
        for y in range(0,4):
            for x in range(0,4):
                if self.board[y][x] == 0:
                    open_cells += 1
        return open_cells

    def sort_snake(self):
        sorted_list = []
        for y in range(4):
            for x in range(4):
                sorted_list.append(self.board[y][x])
        sorted_list.sort()
        sorted_list.reverse()

        h_value = 0
        #Give no credit if this pattern leads to a gameover
        if self.is_game_over():
            return 0

        #Give bonuses for a snake-look-alike order
        #Where the highest tile is in the top left corner
        for i in range(3):
            h_value += self.board[3][i] * 30 * pow(0.8, i)

        h_value += self.board[3][0]*20

        if self.board[3][0] == sorted_list[0] or sorted_list[0] > 500:
            for i in range(3):
                h_value += self.board[2][3-i] * 6 * pow(0.5, i)
        else:
            for i in range(3):
                h_value += self.board[2][i] * 6 * pow(0.5, i)

        return h_value

    def gradient(self):
        h_value_sw = 0
        h_value_se = 0
        h_value_nw = 0
        h_value_ne = 0
        for y in range(0, 4):
            for x in range(0, 4):
                # h_value_sw += self.board[y][x] * 0.5**(y + x)
                # h_value_se += self.board[y][x] * 0.5**(y + (3-x))
                # h_value_nw += self.board[y][x] * 0.5**((3-y) + x)
                if x > y:
                    h_value_nw += self.board[y][x] * (0.5**((3-y) + x)) * 1.1
                else:
                    h_value_nw += self.board[y][x] * (0.5**((3-y) + x))
                # h_value_ne += self.board[y][x] * 0.5**((3-y) + (3-x))

        #return max(h_value_sw, h_value_se, h_value_nw, h_value_ne)
        return h_value_nw

    def print_board(self):
        # self.board = [[2,0,0,2],[2,2,2,2],[0,0,2,2],[2,0,0,0]]
        for row in range(3,-1,-1):
            print self.board[row]