import abc

class BaseCSP(object):
    def __init__(self):
        __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def init_revise_queue(self, constraints, variable_dict):
        return

    @abc.abstractmethod
    def domain_filtering_loop(self, variable_dict):
        return


    @abc.abstractmethod
    def revise(self, variable, constr, variable_dict):
        return