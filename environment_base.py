__author__ = 'hakon0601'

import abc


class BaseEnvironment(object):
    __metaclass=abc.ABCMeta
    @abc.abstractmethod
    def get_start_node(self):
        return

    @abc.abstractmethod
    def print_board(self):
        return

    @abc.abstractmethod
    def get_successor_nodes(self, node):
        return

    @abc.abstractmethod
    def dist_between(self, node, successor):
        return


