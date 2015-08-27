__author__ = 'hakon0601'

import abc


class BaseEnvironment(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_start_node(self):
        return

    @abc.abstractmethod
    def get_goal_node(self):
        return

    @abc.abstractmethod
    def get_successor_nodes(self, node):
        return

    @abc.abstractmethod
    def movement_cost(self, node, successor):
        return

    @abc.abstractmethod
    def reconstruct_path(self, node):
        return
