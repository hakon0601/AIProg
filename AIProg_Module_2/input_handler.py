
import variable
import constraint

def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    #k = int(raw_input("k: "))
    # TODO
    k = 3

    variable_dict = {}

    nr_of_variables, nr_of_constraints = map(int, content[0].rstrip().split(" "))
    # Reads all the variables into a variable dictionary.
    # key = variable index and value = Variable object
    for i in range(1, nr_of_variables + 1):
        vertex_info = map(float, content[i].rstrip().split(" "))
        v = variable.Variable(index=int(vertex_info[0]), x=vertex_info[1], y=vertex_info[2], k=k)
        variable_dict[v.index] = v

    constraints = []
    # Reads all constraints into a list containing Constraint objects
    for j in range(i + 1, nr_of_variables + nr_of_constraints + 1):
        constraint_info =  map(int, content[j].rstrip().split(" "))
        variables_involved_in_constraint = [variable_dict[constraint_info[0]], variable_dict[constraint_info[1]]]
        constraints.append(constraint.Constraint(variables_involved_in_constraint))

    return variable_dict, constraints

#Take board spesification from user via command line
def prompt_user_input(board):
    raise NotImplementedError

