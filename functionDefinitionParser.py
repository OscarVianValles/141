from parser import Parser
from state import State
import tokenize


class FunctionDefinitionParser(Parser):
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

        # Store parameters in a separate list
        self.__tokens[2] = self.__tokens[2].split(",")

        # Tokenize parameters by their type and var name
        self.__tokens[2] = [param.strip().split(" ") for param in self.__tokens[2]]

        # If { is not found in the fourth token, then that means extra parentheses
        # were added to the function, making it invalid
        if "{" not in self.__tokens[3]:
            self.__tokens.clear()
            self.__validity = False
            return

        self.__tokens = tokenize.inPlace(self.__tokens, 3, "}")
        self.__tokens = tokenize.inPlace(self.__tokens, 3, "{")

        # If self.__tokens[3] or self.__tokens[5] is not empty, then that means
        # there are extra stuff before and after the function declaration
        if self.__tokens[3] != "" or self.__tokens[5] != "":
            self.__tokens.clear()
            self.__validity = False
            return

        self.__tokens.pop(5)
        self.__tokens.pop(3)

        self.__tokens[3] = self.__tokens[3].split(";")
        self.__tokens[3] = [line.strip() for line in self.__tokens[3]]

    def tokens(self):
        return self.__tokens

    def changeState(self, newState):
        self.__state = newState

    def incrementCurrWord(self):
        self.__currWord += 1

    def check(self):
        # If self.__validity is set to False, then it was already found to be invalid in
        # the tokenizing phase, so skip going through the states
        if self.__validity is None:
            currState = False
            while not currState:
                currState = self.__state.check()
            self.__validity = self.__state.output()

        return self.__validity


class State0(State):
    def __init__(self, parser: "Parser"):
        self.__parser: "Parser" = parser
        self.__output: bool = False

    def check(self):
        return False

    def output(self) -> bool:
        return self.__output


# Sources:
# isinstance: https://stackoverflow.com/questions/26544091/checking-if-type-list-in-python
# None: https://stackoverflow.com/questions/3289601/null-object-in-python
