from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def output(self):
        pass
