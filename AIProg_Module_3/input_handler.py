from variable import Variable
from constraint import Constraint

def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    nr_of_columns, nr_of_rows = map(int, content[0].rstrip().split(" "))
    print "number of rows: " + str(nr_of_rows)
    print "number of columns: " + str(nr_of_columns)
    domain = (nr_of_columns, nr_of_rows)

    variable_dict = {}
    constraints = []

    # Add all row segments as variables
    for i in range(1, nr_of_rows+1):

        index = i-1
        segments = map(int, content[i].rstrip().split(" "))
        segments_on_that_row = []
        for j in range(len(segments)):
            # segments[j] is the segment length
            # nr_of_columns = domain = possible start points. Initial: All possibilities
            variable = Variable("row", index, str(j), segments[j], nr_of_columns)
            variable_dict[variable] = variable
            segments_on_that_row.append(variable)
        # Create a constraint for each neighbour pair of segments
        seg_count = len(segments_on_that_row)
        #print "row number " + str(index) + ":"
        for k in range(seg_count):
            if k+1 < seg_count:
                c = Constraint(variable_dict, [segments_on_that_row[k], segments_on_that_row[k+1]])
                constraints.append(c)
                #print(c)
            else:
                break

    # Add all column segments as variables
    for i in range(nr_of_rows+1, nr_of_rows+nr_of_columns+1):
        index = nr_of_rows+nr_of_columns-i
        print "INDEX: " + str(index)
        segments = map(int, content[i].rstrip().split(" "))
        print segments
        segments_on_that_column = []
        for j in range(len(segments)):
            # segments[j] is the segment length
            # nr_of_columns = domain = possible start points
            variable = Variable("column", index, str(j), segments[j], nr_of_rows)
            variable_dict[variable] = variable
            segments_on_that_column.append(variable)
        # Create a constraint for each neighbour pair of segments
        seg_count = len(segments_on_that_column)
        #print "column number " + str(index) + ":"
        for k in range(seg_count):
            if k+1 < seg_count:
                c = Constraint(variable_dict, [segments_on_that_column[k], segments_on_that_column[k+1]])
                constraints.append(c)
                #print(c)
            else:
                break

    return domain, variable_dict, constraints