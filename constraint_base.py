import abc


class BaseConstraint(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __str__(self):
        return

    @abc.abstractmethod
    def __repr__(self):
        return