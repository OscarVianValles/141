from parser import Parser
from state import State
from constants import constants
import string
import tokenize


class FunctionDeclarationParser(Parser):
    def __init__(self, testCase: [str]):
        self.__tokens: [str] = testCase
        self.__state: "State" = State0(self)
        self.__params: [str] = []
        self.__functions: [str] = []
        self.__maxFunctions: int = 0

        try:
            self.__tokenize()
        except IndexError:
            self.__tokens.clear()
            self.__validity = False

    def __tokenize(self):
        # Separate leading data type
        self.__tokens = self.__tokens[0].split(" ", 1)

        # Separate the different functions
        self.__tokens[1] = self.__tokens[1].split("),")

        # Add parenthesis back to all tokens except last
        self.__tokens[1][0 : len(self.__tokens[1]) - 1] = [
            token + ")" for token in self.__tokens[1][0 : len(self.__tokens[1]) - 1]
        ]

        # Separate the closing parenthesis and the rest of the test case so that
        # If there are other parts of the test case, they won't be included in the
        # parameters list
        self.__tokens[1] = [token.split(")") for token in self.__tokens[1]]

        # Separate function name
        self.__tokens[1] = [
            tokenize.inPlace(token, 0, "(") for token in self.__tokens[1]
        ]

        # Store parameters in a separate list and clean up leading and trailing white space
        for token in self.__tokens[1]:
            token[1] = token[1].split(",")
            token[1] = [param.strip().split(" ") for param in token[1]]

        for token in self.__tokens:
            if not isinstance(token, list):
                token = token.strip()

        self.__maxFunctions = len(self.__tokens[1])

    def tokens(self):
        return self.__tokens

    def params(self):
        return self.__params

    def functions(self):
        return self.__functions

    def maxFunctions(self):
        return self.__maxFunctions

    def addFunction(self, function: str):
        self.__functions.append(function)

    def addParams(self, param):
        self.__params.append(param)

    def clearParams(self):
        self.__params.clear()

    def changeState(self, newState):
        self.__state = newState

    def incrementCurrWord(self):
        self.__currWord += 1

    def check(self):
        currState = False
        while not currState:
            currState = self.__state.check()

        return (
            "Valid Function Declaration"
            if self.__state.output()
            else "Invalid Function Declaration"
        )


class State0(State):
    def __init__(self, parser: "Parser"):
        self.__parser: "Parser" = parser
        self.__output: bool = False

    def check(self):
        # Check if the datatype of the function is valid
        if self.__parser.tokens()[0] not in constants["functionDataTypes"]:
            return True

        self.__parser.changeState(State1(self.__parser, 0))
        return False

    def output(self) -> bool:
        return self.__output


# Checking if function name is already declared and is valid
class State1(State):
    def __init__(self, parser: "Parser", currFunction: int):
        self.__parser: "Parser" = parser
        self.__currFunction: int = currFunction
        self.__output: bool = False

    def check(self) -> bool:
        # If empty, stop
        if self.__parser.tokens()[1][self.__currFunction] == "":
            return True

        # Check if function name has already been declared
        for function in self.__parser.functions():
            if self.__parser.tokens()[1][self.__currFunction] == function:
                return True

        # Check if all letters are valid
        for letter in self.__parser.tokens()[1][self.__currFunction][0]:
            if not (
                letter in string.ascii_letters
                or letter in string.digits
                or letter == "_"
            ):
                return True

        # Check if reserved keywords are not being used:
        for keyword in constants["reserved"]:
            if self.__parser.tokens()[1][self.__currFunction][0] == keyword:
                return True

        self.__parser.addFunction(self.__parser.tokens()[1][self.__currFunction][0])

        # Check Parameters
        self.__parser.changeState(State2(self.__parser, self.__currFunction, 0))
        return False

    def output(self) -> bool:
        return self.__output


# Check param datatype
class State2(State):
    def __init__(self, parser: "Parser", currFunction: int, currParam: int):
        self.__parser: "Parser" = parser
        self.__currFunction: int = currFunction
        self.__currParam: int = currParam
        self.__output: bool = False

    def check(self) -> bool:
        # If no params, go to check semicolon OR go to next function to check
        if self.__parser.tokens()[1][self.__currFunction][1][self.__currParam][0] == "":
            self.__parser.changeState(State4(self.__parser, self.__currFunction))
            return False

        # If datatype exists, check if it is a valid datatype
        if (
            self.__parser.tokens()[1][self.__currFunction][1][self.__currParam][0]
            not in constants["dataTypes"]
        ):
            return True

        # If the length of the current param is > 1, check the validity of the name
        if len(self.__parser.tokens()[1][self.__currFunction][1][self.__currParam]) > 1:
            self.__parser.changeState(
                State3(self.__parser, self.__currFunction, self.__currParam)
            )

        # Else, check the semicolon or the next function to check
        else:
            self.__parser.changeState(State4(self.__parser, self.__currFunction))

        return False

    def output(self) -> bool:
        return self.__output


# Check param name
class State3(State):
    def __init__(self, parser: "Parser", currFunction: int, currParam: int):
        self.__parser: "Parser" = parser
        self.__currFunction: int = currFunction
        self.__currParam: int = currParam
        self.__output: bool = False

    def check(self) -> bool:
        # If assignment operator was called but it is empty, return invalid
        if self.__parser.tokens()[1][self.__currFunction][1][self.__currParam][1] == "":
            return True

        # Check if param is already declared
        for param in self.__parser.params():
            if (
                self.__parser.tokens()[1][self.__currFunction][1][self.__currParam][1]
                == param
            ):
                return True

        # Check if the param name is using valid characters
        for char in self.__parser.tokens()[1][self.__currFunction][1][self.__currParam][
            1
        ]:
            if not (
                char in string.ascii_letters or char in string.digits or char == "_"
            ):
                return True

        # Add Params to the list
        self.__parser.addParams(
            self.__parser.tokens()[1][self.__currFunction][1][self.__currParam][1]
        )

        if self.__currParam < len(self.__parser.tokens()[1][self.__currFunction]) - 1:
            self.__parser.changeState(
                State2(self.__parser, self.__currFunction, self.__currParam + 1)
            )
        else:
            self.__parser.changeState(State4(self.__parser, self.__currFunction))
        return False

    def output(self) -> bool:
        return self.__output


# Check semicolon and go to next function if it exists
class State4(State):
    def __init__(self, parser: "Parser", currFunction: int):
        self.__parser: "Parser" = parser
        self.__currFunction: int = currFunction
        self.__output: bool = False

    def check(self) -> bool:
        # Delete Params list
        self.__parser.clearParams()

        if self.__currFunction < self.__parser.maxFunctions() - 1:
            if self.__parser.tokens()[1][self.__currFunction][2] != "":
                return True

            self.__parser.changeState(State1(self.__parser, self.__currFunction + 1))
            return False

        else:
            if self.__parser.tokens()[1][self.__currFunction][2] != ";":
                return True

        self.__output = True
        return True

    def output(self) -> bool:
        return self.__output


# Parser contents
# self.__parser.tokens()[0] : srt = Datatype
# self.__parser.tokens()[1][0] : str = Function Name
# self.__parser.tokens()[1][1] : [[str]] = parameters
# self.__parser.tokens()[1][1][n] : [str] parameter
# self.__parser.tokens()[1][1][n][0] : str = parameter datatype
# self.__parser.tokens()[1][1][n][1] : str = parameter name
# self.__parser.tokens()[1][2] : semicolon
