import abc

class Worker:
    @abc.abstractmethod
    def work():
        raise NotImplementedError(
            'Virtual method work was not overwritten'
        )
