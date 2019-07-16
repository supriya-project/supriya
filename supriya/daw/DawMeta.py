import abc


class DawMeta(abc.ABCMeta):

    ### CONSTRUCTOR ###

    def __new__(metaclass, class_name, bases, namespace):
        return super().__new__(metaclass, class_name, bases, namespace)
