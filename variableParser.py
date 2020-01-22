from parser import Parser
from state import State
import tokenize


class VariableParser(Parser):
    def __init__(self, testCase: [str]):
        self.__tokens: [str] = testCase
        self.__state: "State" = State0(self)
        self.__currWord: int = 0

        self.__tokenize()

    def __tokenize(self):
        # Separate leading data type
        self.__tokens = self.__tokens[0].split(" ", 1)

        # Tokenize the variables and place them at the same place
        self.__tokens = tokenize.inPlace(self.__tokens, 1, ",")

        # strip tokens to remove extra white space
        self.__tokens = [token.strip() for token in self.__tokens if token != ""]

    # Public
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
