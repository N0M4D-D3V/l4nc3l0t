import abc


class AbstractStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set_up(self, dataframe):
        raise NotImplementedError

    @abc.abstractmethod
    def check_long_signal(self, i):
        raise NotImplementedError

    @abc.abstractmethod
    def check_short_signal(self, i):
        raise NotImplementedError

    @abc.abstractmethod
    def param_request(self):
        raise NotImplementedError
