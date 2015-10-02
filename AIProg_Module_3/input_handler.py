from variable import Variable
from constraint import Constraint

def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    nr_of_columns, nr_of_rows = map(int, content[0].rstrip().split(" "))
    print "number of rows: " + str(nr_of_rows)
    print "number of columns: " + str(nr_of_columns)
    dimensions = (nr_of_columns, nr_of_rows)

    variable_dict = {}
    constraints = []

    variable_index = 0
    # Add all row segments as variables
    for i in range(1, nr_of_rows+1):

        segments = map(int, content[i].rstrip().split(" "))
        segments_on_that_row = []
        for j in range(len(segments)):
            variable = Variable(index=variable_index, direction="row", line_index=i-1, segment_nr=j, length=segments[j], k=nr_of_columns)
            variable_index += 1
            variable_dict[variable_index] = variable
            segments_on_that_row.append(variable)
        # Create a constraint for each neighbour pair of segments
        seg_count = len(segments_on_that_row)
        #print "row number " + str(index) + ":"
        for seg_i in range(seg_count - 1):
            # Creating constraints between segments on the same row
            c = Constraint(variable_dict, [variable_index - 2 - seg_i, variable_index - 1 - seg_i ])
            constraints.append(c)

    # Add all column segments as variables
    for i in range(nr_of_rows+1, nr_of_rows+nr_of_columns+1):
        line_index = i - nr_of_rows - 1
        #print "INDEX: " + str(index)
        segments = map(int, content[i].rstrip().split(" "))
        #print segments
        segments_on_that_column = []
        for j in range(len(segments)):
            # segments[j] is the segment length
            variable = Variable(index=variable_index, direction="column", line_index=line_index, segment_nr=j, length=segments[j], k=nr_of_rows)
            variable_index += 1
            variable_dict[variable_index] = variable
            segments_on_that_column.append(variable)
        # Create a constraint for each neighbour pair of segments
        seg_count = len(segments_on_that_column)
        #print "column number " + str(index) + ":"
        for seg_i in range(seg_count - 1):
            c = Constraint(variable_dict, [variable_index - 2 - seg_i, variable_index - 1 - seg_i ])
            constraints.append(c)
    print(constraints)

    return dimensions, variable_dict, constraints