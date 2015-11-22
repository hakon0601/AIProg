import json
import random

FILENAME = "nn_cases_gradient.txt"


def process_cases_for_nn(nr_of_cases=1, test=False):
    # The cases loaded are for some reason not the same each time
    case_dict = load_cases()
    inputs = list(case_dict.keys())
    labels = list(case_dict.values())
    print("Number of available cases", len(inputs))

    for i in range(len(inputs)):
        inputs[i] = list(map(int, inputs[i].replace("[", "").replace("]", "").split(", ")))

    if test:
        # The test set is the last cases in the set
        return inputs[len(inputs) - nr_of_cases:len(inputs)], labels[len(inputs) - nr_of_cases:len(inputs)]
        #start_index = random.randrange(0, len(labels) - nr_of_cases - 2)
        #return inputs[start_index:(start_index +nr_of_cases)], labels[start_index:(start_index + nr_of_cases)]
    else:
        return inputs[0:nr_of_cases], labels[0:nr_of_cases]


def load_cases():
    return json.load(open(FILENAME))


def dump_cases(cases):
    json.dump(cases, open(FILENAME, 'w'))