from functionDeclarationParser import FunctionDeclarationParser
from functionDefinitionParser import FunctionDefinitionParser
from variableParser import VariableParser


def tokenizeFile() -> [[str]]:
    # Open File
    with open("mpa1.in") as file:
        # Read file
        inputString: str = file.read()

        # Strip Whitespace
        inputString = inputString.replace("\r", "")
        inputString = inputString.replace("\n", "")

        # Separate Testcases
        testCases: [str] = inputString.split("#")

        # Cleanup Empty Testcases
        testCases = [testCase for testCase in testCases if testCase != ""]

        # Create blank parsers list
        parsers: ["parser"] = []

        # Create
        for testCase in testCases:
            if "{" in testCase:
                parsers.append(FunctionDeclarationParser([testCase]))
            elif "(" in testCase:
                parsers.append(FunctionDefinitionParser([testCase]))
            else:
                parsers.append(VariableParser([testCase]))

        return parsers


def main():
    parsers = tokenizeFile()
    for parser in parsers:
        print(parser.tokens())


if __name__ == "__main__":
    main()
