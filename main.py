__author__ = 'hakon0601'

import board
import a_star
from gui import Gui

board = board.Board("board6")
board.print_board()

a_star = a_star.AStar()

gui = Gui(board)
gui.mainloop()

end_node = a_star.generic_algorithm(board)
if end_node:
    print("Success")
    board.reconstruct_path(end_node)
    board.print_board()
else:
    print("Failed")






