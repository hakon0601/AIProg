
import variable
import constraint

def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    #k = int(raw_input("k: "))
    # TODO
    k = 4

    variable_dict = {}

    nr_of_variables, nr_of_constraints = map(int, content[0].rstrip().split(" "))
    for i in range(1, nr_of_variables + 1):
        vertex_info = map(float, content[i].rstrip().split(" "))
        v = variable.Variable(index=int(vertex_info[0]), x=vertex_info[1], y=vertex_info[2], k=k)
        variable_dict[v.index] = v

    constraints = []
    for j in range(i + 1, nr_of_variables + nr_of_constraints + 1):
        constraint_info =  map(int, content[j].rstrip().split(" "))
        constraints.append(constraint.Constraint(index_1=constraint_info[0], index_2=constraint_info[1]))

    return variable_dict, constraints

#Take board spesification from user via command line
def prompt_user_input(board):
    raise NotImplementedError

