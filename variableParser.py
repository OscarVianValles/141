from parser import Parser
from state import State
from constants import constants
import string


class VariableParser(Parser):
    def __init__(self, testCase: [str]):
        self.__tokens: [str] = testCase
        self.__state: "State" = State0(self)
        self.__vars: [str] = []

        self.__tokenize()

    def __tokenize(self):
        # Separate leading data type
        self.__tokens = self.__tokens[0].split(" ", 1)

        # Remove space, split the variable declarations then strip them
        self.__tokens[1] = self.__tokens[1].replace(" ", "").split(",")
        self.__tokens[1] = [
            variable.strip().split("=")
            for variable in self.__tokens[1]
            if variable != " "
        ]

        self.__maxWords = len(self.__tokens[1])

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

        return (
            "Valid Variable Declaration"
            if self.__state.output()
            else "Invalid Variable Declaration"
        )


# Check if the first token is a datatype
class State0(State):
    def __init__(self, parser: "Parser"):
        self.__parser: "Parser" = parser
        self.__output: bool = False

    def check(self) -> bool:
        for dataType in constants["dataTypes"]:
            if dataType in self.__parser.tokens()[0]:
                self.__parser.changeState(State1(self.__parser, 0))
                return False

        # Checking is done
        return True

    def output(self) -> bool:
        return self.__output


# Checking if variable declaration contains reserved keywords
class State1(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        for keyword in constants["reserved"]:
            for i in range(0, len(self.__parser.tokens()[1][self.__currWord])):
                if keyword in self.__parser.tokens()[1][self.__currWord][i]:
                    # If keyword is found, then checking is done
                    return True

        self.__parser.changeState(State2(self.__parser, self.__currWord))
        return False

    def output(self) -> bool:
        return self.__output


# Checking if name is valid
class State2(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        for letter in self.__parser.tokens()[1][self.__currWord][0]:
            if (
                letter not in string.ascii_letters
                and letter not in string.digits
                and not "_"
                and not ";"
            ):
                return True

        if len(self.__parser.tokens()[1][self.__currWord]) > 1:
            self.__parser.changeState(State3(self.__parser, self.__currWord))
        else:
            self.__parser.changeState(State3(self.__parser, self.__currWord))
        return False

    def output(self) -> bool:
        return self.__output


class State3(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        self.__output = True
        return True

    def output(self) -> bool:
        return self.__output


# Parser contents
# self.__parser.tokens()[0] : string is the datatype
# self.__parser.tokens()[1] : [[str]] is the variables.
# self.__parser.tokens()[1][n] : [str] is the single variable
# self.__parser.tokens()[1][n][0] : str is the variable name
# self.__parser.tokens()[1][n][1] : str is the value if it exists
