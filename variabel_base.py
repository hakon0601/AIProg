import abc

# TODO Kan jeg fjerne denne klassen? den har ikke lenger noen funksjonell verdi

class BaseVariabel(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __str__(self):
        return

    @abc.abstractmethod
    def __repr__(self):
        return

    #@abc.abstractmethod
    #def __eq__(self, other):
    #    return