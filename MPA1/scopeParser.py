from parser import Parser
from constants import constants
from variableParser import VariableParser


class ScopeParser(Parser):
    def __init__(
        self,
        testCase: [str],
        outerScopeVariables: [[str]],
        toBeParsed: [str],
        functionReturnType: str,
    ):
        self.__tokens: [str] = testCase
        self.__currLine: int = 0
        self.__validity: bool = True
        self.__vars: [[str]] = outerScopeVariables
        self.__parsers: ["Parser"] = []
        self.__bracePairs = []
        self.__toBeParsed = toBeParsed
        self.__functionReturnType = functionReturnType

        self.__tokenize()

    def __tokenize(self):
        bracesStackCheck = []

        # Get all braces
        for i in range(len(self.__tokens[0])):
            letter = self.__tokens[0][i]
            if letter == "{":
                bracesStackCheck.append([i, -1])
            elif letter == "}":
                try:
                    bracesStackCheck[-1][-1] = i + 1
                    self.__bracePairs.insert(0, bracesStackCheck[-1])
                    bracesStackCheck.pop()
                except IndexError:
                    self.__validity = False

        count: int = 0

        while len(self.__bracePairs) > 1:
            # Append scope to be parsed
            self.__toBeParsed.append(
                self.__tokens[0][self.__bracePairs[-1][0] : self.__bracePairs[-1][1]]
            )

            # Remove from token but add place holder text
            self.__tokens[0] = (
                self.__tokens[0][: self.__bracePairs[-1][0]]
                + "{}#;".format(count)
                + self.__tokens[0][self.__bracePairs[-1][1] :]
            )

            # Get the length of the removed string
            removedStringLen: int = len(self.__toBeParsed[-1]) - len(
                "{}#;".format(count)
            )
            tempPair = self.__bracePairs.pop()

            # Correct brace pair numbers
            for bracePair in self.__bracePairs:
                if bracePair[0] > tempPair[0]:
                    bracePair[0] -= removedStringLen

                bracePair[1] -= removedStringLen

            count += 1

        # Remove leading and trailing brackets of the scope. If the leading and trailing brackets are
        # not found in the first and last element, then it is deemed as invalid
        if self.__bracePairs[0][0] == 0 and self.__bracePairs[0][1] == len(
            self.__tokens[0]
        ):
            self.__tokens[0] = self.__tokens[0][
                self.__bracePairs[0][0] + 1 : self.__bracePairs[0][1] - 1
            ].strip()
        else:
            self.__validity = False

        self.__bracePairs.clear()

        self.__tokens = self.__tokens[0].split(";")
        self.__tokens = [token.strip() for token in self.__tokens if token != ""]

    def tokens(self):
        return self.__tokens

    def changeState(self, newState):
        self.__state = newState

    def incrementCurrWord(self):
        self.__currWord += 1

    def check(self):
        parser: "Parser" = ""
        for token in self.__tokens:
            if token[-1] == "#":
                iterator: int = 0
                try:
                    iterator = int(token[0:-1])
                    parser = ScopeParser(
                        [self.__toBeParsed[iterator].strip()],
                        self.__vars,
                        self.__toBeParsed,
                        self.__functionReturnType,
                    )
                except ValueError:
                    self.__validity = False
                    break

            elif token.split()[0] in constants["dataTypes"]:
                parser = VariableParser(
                    [token + ";"], [var[1] for var in self.__vars], False
                )
                parser.check()
                self.__vars.extend(parser.fullVars())

            elif token.split()[0] == "return":
                if (
                    "+" in token
                    or "-" in token
                    or "*" in token
                    or "/" in token
                    or "%" in token
                ) and "=" not in token:
                    # Sorry po sir
                    token = "return oscarTestVar =" + token[6:]
                    self.__vars.append(["int", "oscarTestVar"])

                parser = VariableParser(
                    [token + ";"], [var[1] for var in self.__vars], True
                )
                if self.__functionReturnType == "void" and len(parser.tokens()) > 1:
                    self.__validity = False
                    break
            else:
                parser = VariableParser(
                    ["return " + token + ";"], [var[1] for var in self.__vars], True
                )

            self.__validity = self.__validity and parser.check()
            if self.__validity is False:
                break

        return self.__validity

    def checkPretty(self):
        pass


# Sources:
# isinstance: https://stackoverflow.com/questions/26544091/checking-if-type-list-in-python
# None: https://stackoverflow.com/questions/3289601/null-object-in-python
