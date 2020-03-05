#ifndef NFA_H
#define NFA_H

enum nfaType { _concat, _union, _end };

class State {
  nfaType type;
  State &top;
  State &bottom;
};

#endif
