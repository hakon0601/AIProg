
def read_file(board, filename):
    with open(filename) as f:
        content = f.readlines()

    dim = content[0][1: len(content[0]) - 2].split(",")
    board.dim = (int(dim[0]), int(dim[1]))
    start_goal = content[1].strip().replace(")(", ",").replace("(", "").replace(")", "").split(",")
    board.start = (int(start_goal[0]), int(start_goal[1]))
    board.goal = (int(start_goal[2]), int(start_goal[3]))

    # parsing obstacles
    for i in range(2, len(content)):
        obstacle_row = map(int, content[i].rstrip()[1:-1].split(","))
        # Adding arrays with 4 values to the obstacle list.
        # X, Y, width, height
        board.obstacles.append([obstacle_row[0], obstacle_row[1], obstacle_row[2], obstacle_row[3]])

#Take board spesification from user via command line
def prompt_user_input(board):
    raise NotImplementedError