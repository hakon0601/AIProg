from variable import Variable
from constraint_row_var_approach import ConstraintRowVarApproach

def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    nr_of_columns, nr_of_rows = map(int, content[0].rstrip().split(" "))
    print "number of rows: " + str(nr_of_rows)
    print "number of columns: " + str(nr_of_columns)
    dimensions = (nr_of_columns, nr_of_rows)

    variable_dict = {}
    rows = []
    columns = []
    constraints = []

    variable_index = 0
    # Add all rows as variables
    for i in range(1, nr_of_rows+1):
        segments = map(int, content[i].rstrip().split(" "))
        #segments_on_that_row = []
        variable = Variable(index=variable_index, direction="row", nr=variable_index, length=nr_of_columns, segments=segments)
        variable_dict[variable_index] = variable
        variable_index += 1
        rows.append(variable)

    # Add all columns as variables
    for i in range(nr_of_rows+1, nr_of_rows+nr_of_columns+1):
        segments = map(int, content[i].rstrip().split(" "))
        variable = Variable(index=variable_index, direction="column", nr=i-nr_of_rows-1,length=nr_of_rows, segments=segments[::-1])
        variable_dict[variable_index] = variable
        variable_index += 1
        columns.append(variable)
    for column in columns:
        for row in rows:
            constraints.append(ConstraintRowVarApproach(variable_dict, involved_variables=[column.index, row.index]))

    return dimensions, variable_dict, constraints