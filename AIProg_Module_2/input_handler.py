
import variable
import constraint

def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    filename_k_dict = {"graphs/graph0.txt": 3, "graphs/graph1.txt": 3, "graphs/graph-color-1.txt": 4, "graphs/graph-color-2.txt": 4,
                       "graphs/rand-50-4-color1.txt": 4, "graphs/rand-100-4-color1.txt": 4,
                       "graphs/rand-100-6-color1.txt": 6, "graphs/spiral-500-4-color1.txt": 4}
    #k = int(raw_input("k: "))

    k = filename_k_dict[filename]

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
        #variables_involved_in_constraint = [variable_dict[constraint_info[0]], variable_dict[constraint_info[1]]]
        constraints.append(constraint.Constraint(variable_dict, constraint_info))

    return variable_dict, constraints

#Take board spesification from user via command line
def prompt_user_input(board):
    raise NotImplementedError

