from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def check(self):
        pass
