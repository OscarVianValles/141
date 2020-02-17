from parser import Parser
from state import State
from constants import constants
import string


class VariableParser(Parser):
    def __init__(self, testCase: [str], scopeVars: [str], isReturn: bool):
        self.__tokens: [str] = testCase
        self.__state: "State" = State0(self)
        self.__vars: [str] = scopeVars
        self.__newVars: [str] = []
        self.__maxWords: int = 0
        self.__isReturn = isReturn

        try:
            self.__tokenize()
        except IndexError:
            if not isReturn:
                self.__tokens.clear()

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

    def vars(self):
        return self.__vars

    def fullVars(self):
        return [[self.__tokens[0], var] for var in self.__newVars]

    def maxWords(self):
        return self.__maxWords

    def isReturn(self):
        return self.__isReturn

    def changeState(self, newState: "State"):
        self.__state = newState

    def addVar(self, newVar: str):
        self.__vars.append(newVar)
        self.__newVars.append(newVar)

    def checkPretty(self):
        success = False
        try:
            success = self.check()
        except Exception:
            success = False
        return (
            "Valid Variable Declaration" if success else "Invalid Variable Declaration"
        )

    def check(self):
        currState = False
        while not currState:
            currState = self.__state.check()

        return self.__state.output()


# Check if the first token is a datatype
class State0(State):
    def __init__(self, parser: "Parser"):
        self.__parser: "Parser" = parser
        self.__output: bool = False

    def check(self) -> bool:
        if len(self.__parser.tokens()) == 0:
            return True

        if self.__parser.isReturn():
            if (
                "return" == self.__parser.tokens()[0]
                or "return;" == self.__parser.tokens()[0]
            ):
                if len(self.__parser.tokens()) > 1:
                    self.__parser.changeState(State1(self.__parser, 0))
                    return False
                else:
                    self.__output = True
                    return True
        else:
            for dataType in constants["dataTypes"]:
                if dataType in self.__parser.tokens()[0]:
                    self.__parser.changeState(State1(self.__parser, 0))
                    return False

        return True

    def output(self) -> bool:
        return self.__output


# Checking if variable declaration contains reserved keywords in the assignment and variable name
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


# Checking if variable is already declared
class State2(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        # Check all letters if it is in the allowable characters list
        variable = self.__parser.tokens()[1][self.__currWord][0]
        variable = variable if variable[-1] != ";" else variable[0:-1]
        inVariable: bool = False
        for var in self.__parser.vars():
            if var == variable:
                inVariable = True

        if (not self.__parser.isReturn() and inVariable) or (
            self.__parser.isReturn() and not inVariable
        ):
            return True

        # Go to State4 if it is the last word AND it does not have an assignment function
        if (
            self.__currWord >= self.__parser.maxWords() - 1
            and len(self.__parser.tokens()[1][-1]) <= 1
        ):
            self.__parser.changeState(State4(self.__parser, self.__currWord))
        else:
            self.__parser.changeState(State3(self.__parser, self.__currWord))

        return False

    def output(self) -> bool:
        return self.__output


# Checking if name is valid, if it not the last word in the test case
class State3(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        # If empty, stop
        if self.__parser.tokens()[1][self.__currWord][0] == "":
            return True

        # Check all letters if it is in the allowable characters list
        for letter in self.__parser.tokens()[1][self.__currWord][0]:
            if not (
                letter in string.ascii_letters
                or letter in string.digits
                or letter == "_"
            ):
                return True

        if self.__parser.tokens()[1][self.__currWord][0][0] in string.digits:
            return True

        self.__parser.addVar(self.__parser.tokens()[1][self.__currWord][0])

        # If the more tokens are present, check the validity of the assignment statement,
        # else check the next words
        if len(self.__parser.tokens()[1][self.__currWord]) > 1:
            self.__parser.changeState(State5(self.__parser, self.__currWord))
        else:
            self.__parser.changeState(State1(self.__parser, self.__currWord + 1))

        return False

    def output(self) -> bool:
        return self.__output


# Checking if name is valid and semicolon is found on the last variable
# END STATE 1
class State4(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        # If empty, stop
        if self.__parser.tokens()[1][self.__currWord][0] == "":
            return True

        # Check all letters except the last if the characters are valid
        for i in range(len(self.__parser.tokens()[1][self.__currWord][0]) - 1):
            letter: str = self.__parser.tokens()[1][self.__currWord][0][i]
            if not (
                letter in string.ascii_letters
                or letter in string.digits
                or letter == "_"
            ):
                return True

        if self.__parser.tokens()[1][self.__currWord][0][0] in string.digits:
            return True

        if self.__parser.tokens()[1][self.__currWord][0][-1] == ";":
            self.__parser.addVar(self.__parser.tokens()[1][self.__currWord][0][0:-1])
            self.__output = True
            return True

        return True

    def output(self) -> bool:
        return self.__output


# Checking what type of values in the assignment
class State5(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        # If empty, stop
        if self.__parser.tokens()[1][self.__currWord][1] == "":
            return True

        isLast: bool = self.__currWord == self.__parser.maxWords() - 1

        if (
            "+" in self.__parser.tokens()[1][self.__currWord][1]
            or "-" in self.__parser.tokens()[1][self.__currWord][1]
            or "*" in self.__parser.tokens()[1][self.__currWord][1]
            or "/" in self.__parser.tokens()[1][self.__currWord][1]
            or "%" in self.__parser.tokens()[1][self.__currWord][1]
        ):
            if isLast:
                self.__parser.changeState(State12(self.__parser, self.__currWord))
            else:
                self.__parser.changeState(State13(self.__parser, self.__currWord))

            return False

        # Check if char is being assigned
        if (
            "'" in self.__parser.tokens()[1][self.__currWord][1]
            or '"' in self.__parser.tokens()[1][self.__currWord][1]
        ):
            if isLast:
                self.__parser.changeState(State6(self.__parser, self.__currWord))
            else:
                self.__parser.changeState(State7(self.__parser, self.__currWord))

            return False

        # Check if a variable is being assigned by checking that there exists other characters that are not numbers or a .
        for letter in self.__parser.tokens()[1][self.__currWord][1]:
            if not (letter in string.digits or letter == "." or letter == ";"):
                if isLast:
                    self.__parser.changeState(State8(self.__parser, self.__currWord))
                else:
                    self.__parser.changeState(State9(self.__parser, self.__currWord))
                return False

        # If both checks failed, then a number is being assigned
        if isLast:
            self.__parser.changeState(State10(self.__parser, self.__currWord))
        else:
            self.__parser.changeState(State11(self.__parser, self.__currWord))

        return False

    def output(self) -> bool:
        return self.__output


# Character Check
# END STATE 2
class State6(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        if (
            self.__parser.tokens()[1][self.__currWord][1][0]
            != self.__parser.tokens()[1][self.__currWord][1][-2]
            or len(self.__parser.tokens()[1][self.__currWord][1]) != 4
            or self.__parser.tokens()[1][self.__currWord][1][-1] != ";"
        ):
            return True

        self.__output = True
        return True

    def output(self) -> bool:
        return self.__output


# Character Check
class State7(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        # Check if the opening and closing apostrophe is the same and if the length of the character is exactly 3
        if (
            self.__parser.tokens()[1][self.__currWord][1][0]
            != self.__parser.tokens()[1][self.__currWord][1][-1]
            or len(self.__parser.tokens()[1][self.__currWord][1]) != 3
        ):
            return True

        # Go to next word
        self.__parser.changeState(State1(self.__parser, self.__currWord + 1))
        return False

    def output(self) -> bool:
        return self.__output


# Variable Check
# END STATE 3
class State8(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        # Get var without semicolon, check if it was declared, and check if it is not the same variable as it was assigned to
        var = self.__parser.tokens()[1][self.__currWord][1][0:-1]
        if (
            var in self.__parser.vars()
            and var != self.__parser.tokens()[1][self.__currWord][1]
            and self.__parser.tokens()[1][self.__currWord][1][-1] == ";"
        ):
            self.__output = True
            return True

        return True

    def output(self) -> bool:
        return self.__output


# Variable Check
class State9(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        # Check if var was declared, and check if it is not the same variable as it was assigned to
        if (
            self.__parser.tokens()[1][self.__currWord][1] in self.__parser.vars()
            and self.__parser.tokens()[1][self.__currWord][0]
            != self.__parser.tokens()[1][self.__currWord][1]
        ):
            self.__parser.changeState(State1(self.__parser, self.__currWord + 1))
            return False

        return True

    def output(self) -> bool:
        return self.__output


# Number Check
# END STATE 4
class State10(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        number = self.__parser.tokens()[1][self.__currWord][1][0:-1]
        if (
            number.count(".") > 1
            or self.__parser.tokens()[1][self.__currWord][1][-1] != ";"
        ):
            return True

        self.__output = True
        return True

    def output(self) -> bool:
        return self.__output


# Variable Check
class State11(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        if self.__parser.tokens()[1][self.__currWord][1].count(".") > 1:
            return True

        self.__parser.changeState(State1(self.__parser, self.__currWord + 1))
        return False

    def output(self) -> bool:
        return self.__output


class State12(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        currArgs = self.__parser.tokens()[1][self.__currWord][1]
        currArgs = currArgs.replace("+", "*")
        currArgs = currArgs.replace("-", "*")
        currArgs = currArgs.replace("/", "*")
        currArgs = currArgs.replace("%", "*")
        currArgs = currArgs.replace("(", "*")
        currArgs = currArgs.replace(")", "*")
        currArgs = currArgs.strip().split("*")
        currArgs = [arg.strip() for arg in currArgs]

        # Check if last character is a semicolon
        if currArgs[-1][-1] != ";":
            return True
        else:
            # Correct semicolon
            currArgs[-1] = currArgs[-1][:-1]

        for i in range(len(currArgs)):
            if "'" in currArgs[i] or '"' in currArgs[i]:
                if currArgs[i][0] != currArgs[i][-1] or len(currArgs[i]) != 3:
                    return True
            else:
                isVar: bool = False
                # Check if the item to be operated on is a variable
                for j in range(len(currArgs[i])):
                    letter = currArgs[i][j]
                    if not (letter in string.digits or letter == "." or letter == ";"):
                        isVar = True

                if isVar:
                    if currArgs[i] not in self.__parser.vars():
                        return True

        self.__output = True
        return True

    def output(self) -> bool:
        return self.__output


class State13(State):
    def __init__(self, parser: "Parser", currWord: int):
        self.__parser: "Parser" = parser
        self.__currWord: int = currWord
        self.__output: bool = False

    def check(self) -> bool:
        currArgs = self.__parser.tokens()[1][self.__currWord][1]
        currArgs = currArgs.replace("+", "*")
        currArgs = currArgs.replace("-", "*")
        currArgs = currArgs.replace("/", "*")
        currArgs = currArgs.replace("%", "*")
        currArgs = currArgs.replace("(", "*")
        currArgs = currArgs.replace(")", "*")
        currArgs = currArgs.strip().split("*")
        currArgs = [arg.strip() for arg in currArgs]

        for i in range(len(currArgs)):
            if "'" in currArgs[i] or '"' in currArgs[i]:
                if currArgs[i][0] != currArgs[i][-1] or len(currArgs[i]) != 3:
                    return True
            else:
                isVar: bool = False
                # Check if the item to be operated on is a variable
                for j in range(len(currArgs[i])):
                    letter = currArgs[i][j]
                    if not (letter in string.digits or letter == "." or letter == ";"):
                        isVar = True

                if isVar:
                    if currArgs[i] not in self.__parser.vars():
                        return True

        self.__parser.changeState(State1(self.__parser, self.__currWord + 1))
        return False

    def output(self) -> bool:
        return self.__output


# Parser contents
# self.__parser.tokens()[0] : string is the datatype
# self.__parser.tokens()[1] : [[str]] is the variables.
# self.__parser.tokens()[1][n] : [str] is the single variable
# self.__parser.tokens()[1][n][0] : str is the variable name
# self.__parser.tokens()[1][n][1] : str is the value if it exists
