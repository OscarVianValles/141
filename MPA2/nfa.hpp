#ifndef NFA_H
#define NFA_H

#include "state.hpp"

class NFA {
private:
  State *_startState;
  std::list<State *> _endStates;

public:
  NFA();
  NFA(char);
  NFA(State *, std::list<State *>);
  NFA(State *);
  NFA(std::list<State *>);

  State *startState();
  std::list<State *> endStates();
  void addNewState(State *);
  void connectNewNFA(NFA);
};

#endif
