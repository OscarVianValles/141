from parser import Parser
from state import State
import tokenize


class FunctionDeclarationParser(Parser):
    def __init__(self, testCase: [str]):
        self.__tokens: [str] = testCase
        self.__state: "State" = State0(self)
        self.__currWord: int = 0
        self.__validity: bool = None

        self.__tokenize()

    def __tokenize(self):
        # Separate leading data type
        self.__tokens = self.__tokens[0].split(" ", 1)

        # Separate the closing parenthesis and the rest of the test case so that
        # If there are other parts of the test case, they won't be included in the
        # parameters list
        self.__tokens = tokenize.inPlace(self.__tokens, 1, ")")

        # Separate the function name
        self.__tokens = tokenize.inPlace(self.__tokens, 1, "(")

        # Store parameters in a separate list and clean up leading and
        # trailing white space
        self.__tokens[2] = self.__tokens[2].split(",")
        self.__tokens[2] = [token.strip() for token in self.__tokens[2]]
        self.__tokens[2] = [param.strip().split(" ") for param in self.__tokens[2]]

        # Strip all tokens except params
        for token in self.__tokens:
            if not isinstance(token, list):
                token = token.strip()

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
