#ifndef TYPE_H
#define TYPE_H

// Enum to store type and precedence
enum type { _invalid, _close, _open, _empty, _alpha, _union, _concat, _kleene };

extern type getType(char element);
extern char getChar(type element);

#endif
