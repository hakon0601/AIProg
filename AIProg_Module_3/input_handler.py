
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    nr_of_rows, nr_of_columns = map(int, content[0].rstrip().split(" "))

    print nr_of_rows
    print nr_of_columns

    print "row specs: "
    for i in range(1, nr_of_rows+1):
        segment = map(int, content[i].rstrip().split(" "))
        print segment

    print " "
    print "column specs: "
    for i in range(nr_of_rows+1, nr_of_rows+nr_of_columns):
        segment = map(int, content[i].rstrip().split(" "))
        print segment

