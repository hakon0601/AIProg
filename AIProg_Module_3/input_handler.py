from variable import Variable
from constraint import Constraint


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    nr_of_columns, nr_of_rows = map(int, content[0].rstrip().split(" "))
    # (x, y)
    dimensions = (nr_of_columns, nr_of_rows)

    variable_dict = {}
    rows = []
    columns = []
    constraints = []

    variable_index = 0
    # Add all rows as variables
    for i in range(1, nr_of_rows+1):
        segments = map(int, content[i].rstrip().split(" "))
        variable = Variable(index=variable_index, direction="row", direction_nr=variable_index, length=nr_of_columns, segments=segments)
        variable_dict[variable_index] = variable
        variable_index += 1
        rows.append(variable)

    # Add all columns as variables
    for i in range(nr_of_rows+1, nr_of_rows+nr_of_columns+1):
        # Reversing the segments order to make it on the right format
        segments = map(int, content[i].rstrip().split(" "))[::-1]
        variable = Variable(index=variable_index, direction="column", direction_nr=i-(nr_of_rows+1),length=nr_of_rows, segments=segments)
        variable_dict[variable_index] = variable
        variable_index += 1
        columns.append(variable)

    # Creating one constraint for each cell shared by a column and a row
    for column in columns:
        for row in rows:
            constraints.append(Constraint(variable_dict, involved_variables=[column.index, row.index]))

    return dimensions, variable_dict, constraints