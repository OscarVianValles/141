from functionDeclarationParser import FunctionDeclarationParser
from functionDefinitionParser import FunctionDefinitionParser
from variableParser import VariableParser


def tokenizeFile() -> [[str]]:
    # Open File
    with open("mpa1.in") as file:
        # Read file
        inputString: str = file.read()

        # Remove first line that indicates the number of testcases
        inputString = inputString.split("\n", 1)[1]

        # Replace new lines with spaces
        inputString = inputString.replace("\r", " ")
        inputString = inputString.replace("\n", " ")
        inputString = inputString.replace("\t", " ")

        # Remove concurrent spaces
        inputString = " ".join(inputString.split())

        # Separate Testcases
        testCases: [str] = inputString.split("#")

        # Cleanup Empty Testcases
        testCases = [
            testCase for testCase in testCases if (testCase != "" and testCase != " ")
        ]

        # Create blank parsers list
        parsers: ["parser"] = []

        # Create parsers depending on the occurence of specific characters
        for testCase in testCases:
            if "{" in testCase:
                parsers.append(FunctionDefinitionParser([testCase.strip()]))
            elif "(" in testCase and "=" not in testCase:
                parsers.append(FunctionDeclarationParser([testCase.strip()]))
            else:
                parsers.append(VariableParser([testCase.strip()]))

        return parsers


def main():
    parsers = tokenizeFile()
    count = 1
    with open("vallesmpa1.out", "w") as f:
        for parser in parsers:
            print(count)
            count += 1
            print(parser.tokens())
            print(parser.check())
            print("")
            print(parser.check(), file=f)


if __name__ == "__main__":
    main()

# Sources:
# Behavioral Patterns - CMSC 23
# Remove concurrent spaces - https://pythonexamples.org/python-replace-multiple-spaces-with-single-space-in-text-file/
