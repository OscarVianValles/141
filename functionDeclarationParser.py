from parser import Parser
from state import State


class FunctionDeclarationParser(Parser):
    def __init__(self, testCase: [str]):
        self.__tokens: [str] = testCase
        self.__state: "State" = State0(self)
        self.__currWord: int = 0

    def tokens(self):
        return self.__tokens

    def changeState(self, newState):
        self.__state = newState

    def incrementCurrWord(self):
        self.__currWord += 1

    def check(self):
        currState = False
        while not currState:
            currState = self.__state.check()

        return self.__state.output()


class State0(State):
    def __init__(self, parser: "Parser"):
        self.__parser: "Parser" = parser
        self.__output: bool = False

    def check(self):
        return False

    def output(self) -> bool:
        return self.__output
