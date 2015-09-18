
def read_file(board, filename):
    with open(filename) as f:
        content = f.readlines()

    dim = content[0][1: len(content[0]) - 2].split(",")
    board.dim = (int(dim[0]), int(dim[1]))
    start_goal = content[1].strip().replace(")(", ",").replace("(", "").replace(")", "").split(",")
    board.start = (int(start_goal[0]), int(start_goal[1]))
    board.goal = (int(start_goal[2]), int(start_goal[3]))

    # parsing obstacles
    for i in range(len(content) - 2):
        obstacle_row = content[i+2][1:len(content[i+2]) - 2].split(",")
        # Adding arrays with 4 values to the obstacle list.
        # X, Y, width, height
        board.obstacles.append([int(obstacle_row[0]), int(obstacle_row[1]), int(obstacle_row[2]), int(obstacle_row[3])])

#Take board spesification from user via command line
def prompt_user_input(board):
    raise NotImplementedError