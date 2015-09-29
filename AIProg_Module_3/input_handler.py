from variable import Variable
from constraint import Constraint

def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    nr_of_rows, nr_of_columns = map(int, content[0].rstrip().split(" "))

    print str(nr_of_rows) + " - " + str(nr_of_columns)

    variable_dict = {}

    # Add all row segments as variables
    for i in range(1, nr_of_rows+2):
        segments = map(int, content[i].rstrip().split(" "))
        segments_on_that_row = []
        for j in range(len(segments)):
            # i-1 is the index
            # segments[j] is the segment length
            # nr_of_columns = domain = possible start points
            variable = Variable("row", i-1, str(j), segments[j], nr_of_columns)
            #print variable
            variable_dict[variable] = variable
            segments_on_that_row.append(variable)
        # TODO Add constraints
        # Send all segments on that row as parameter to constraint
        # OBS variable_dict is not complete yet
        constraint = Constraint(i-1, variable_dict, segments_on_that_row)

    # Add all column segments as variables
    for i in range(nr_of_rows+1, nr_of_rows+nr_of_columns):
        segments = map(int, content[i].rstrip().split(" "))
        for j in range(len(segments)):
            # i-1 is the index
            # segments[j] is the segment length
            # nr_of_columns = domain = possible start points
            variable = Variable("column", i-nr_of_rows-1, str(j), segments[j], nr_of_rows)
            variable_dict[variable] = variable
            #print variable

    return variable_dict