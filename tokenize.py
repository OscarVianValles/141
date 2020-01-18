# Tokenize string in a specific place in the list, then places it at starting at the
# same position
# https://stackoverflow.com/questions/7376019/list-extend-to-index-inserting-list-elements-not-only-to-the-end


def inPlace(inputString: [str], position: int, delimiter: str) -> [str]:
    inputString[position:position] = inputString.pop(position).split(delimiter)
    return inputString
