from constraint import Constraint
from variable import Variable


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    filename_k_dict = {"graphs/graph0.txt": 3, "graphs/graph1.txt": 3, "graphs/graph-color-1.txt": 4, "graphs/graph-color-2.txt": 4,
                       "graphs/rand-50-4-color1.txt": 4, "graphs/rand-100-4-color1.txt": 4,
                       "graphs/rand-100-6-color1.txt": 6, "graphs/spiral-500-4-color1.txt": 4, "gcolor1.txt": 4, "gcolor2.txt": 4, "gcolor3.txt": 4}
    #k = int(raw_input("k: "))

    #k = filename_k_dict[filename]
    k =4
    variable_dict = {}

    nr_of_variables, nr_of_constraints = map(int, content[0].rstrip().split(" "))
    # Reads all the variables into a variable dictionary.
    # key = variable index and value = Variable object
    for i in range(1, nr_of_variables + 1):
        vertex_info = map(float, content[i].rstrip().split(" "))
        v = Variable(index=int(vertex_info[0]), x=vertex_info[1], y=vertex_info[2], k=k)
        variable_dict[v.index] = v

    constraints = []
    # Reads all constraints into a list containing Constraint objects
    for j in range(i + 1, nr_of_variables + nr_of_constraints + 1):
        constraint_info =  map(int, content[j].rstrip().split(" "))
        constr = Constraint(variable_dict, involved_variables=constraint_info)
        constr.constraining_func = makefunc(var_names=["x", "y"], expression="x != y")
        constraints.append(constr)

    return variable_dict, constraints

#Take graph specification from user via command line
def prompt_user_input(board):
    raise NotImplementedError

def makefunc(var_names, expression):
    args = ""
    for n in var_names:
        args = args + "," + n
    return eval("(lambda " + args[1:] + ": " + expression + ")")
