__author__ = 'hakon0601'

import abc


class AStarGeneral():
    __metaclass__ = abc.ABCMeta

'''4
def agenda_loop(open_list, closed_list):
    if not open_list:
        return None
    X = pop(open_list)
    push(X, closed_list)
    if is_solution(X):
        return (X, "SUCCEED")
    SUCC = generate_all_successors(X)
    for S in SUCC:
'''