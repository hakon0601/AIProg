import abc


class BaseState(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate_h(self, x, y, goal_x, goal_y):
        return

    @abc.abstractmethod
    def movement_cost(self, successor):
        return

    @abc.abstractmethod
    def reconstruct_path(self):
        return

    @abc.abstractmethod
    def generate_successor_nodes(self):
        return

    @abc.abstractmethod
    def get_best_parent(self):
        return

    @abc.abstractmethod
    def getID(self):
        return
