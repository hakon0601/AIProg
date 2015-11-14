import json
import random

def get_cases(nr_of_cases=1, test=False):
    case_dict = {}
    case_dict = json.load(open("nn_cases.txt"))
    inputs = list(case_dict.keys())
    labels = list(case_dict.values())
    if test:
        start_index = random.randrange(0, len(labels) - nr_of_cases - 2)
        return inputs[start_index:(start_index +nr_of_cases)], labels[start_index:(start_index + nr_of_cases)]
    else:
        return inputs[0:nr_of_cases], labels[0:nr_of_cases]