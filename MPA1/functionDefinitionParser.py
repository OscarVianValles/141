from parser import Parser
from functionDeclarationParser import FunctionDeclarationParser
from scopeParser import ScopeParser


class FunctionDefinitionParser(Parser):
    def __init__(self, testCase: [str]):
        self.__tokens: [str] = testCase
        self.__currWord: int = 0
        self.__validity: bool = True

        self.__tokenize()

    def __tokenize(self):
        self.__tokens = self.__tokens[0].split("{", 1)
        self.__tokens[0] += ";"
        self.__tokens[1] = "{" + self.__tokens[1]
        self.__parsers: ["Parser"] = []

        self.__parsers.append(
            FunctionDeclarationParser([self.__tokens[0].strip()], True)
        )
        self.__parsers[0].check()
        self.__parsers.append(
            ScopeParser(
                [self.__tokens[1].strip()],
                self.__parsers[0].fullParams(),
                [],
                self.__parsers[0].dataType(),
            )
        )

    def tokens(self):
        return self.__tokens

    def changeState(self, newState):
        self.__state = newState

    def incrementCurrWord(self):
        self.__currWord += 1

    def check(self):
        # All parsers should be true for the function definition should be true
        for parser in self.__parsers:
            self.__validity = self.__validity and parser.check()
            if not self.__validity:
                break

        return self.__validity

    def checkPretty(self):
        return (
            "Valid Function Definition"
            if self.check()
            else "Invalid Function Definition"
        )


# Sources:
# isinstance: https://stackoverflow.com/questions/26544091/checking-if-type-list-in-python
# None: https://stackoverflow.com/questions/3289601/null-object-in-python
