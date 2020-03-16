#include "type.hpp"

type getType(char element) {
  switch (element) {
  case 'a':
  case 'b':
    return _alpha;

  case 'e':
    return _empty;

  case 'O':
    return _concat;

  case 'U':
    return _union;

  case '*':
    return _kleene;

  case ')':
    return _close;

  case '(':
    return _open;

  default:
    return _invalid;
  }
}

char getChar(type element) {
  switch (element) {
  case _concat:
    return 'O';

  case _union:
    return 'U';

  case _kleene:
    return '*';

  case _close:
    return ')';

  case _open:
    return '(';

  case _empty:
    return 'e';

  default:
    // getChar shouldn't be receiving types that are not of the above
    throw "getChar received non valid type";
  }
}
