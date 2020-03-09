#ifndef NFA_H
#define NFA_H

#include "state.hpp"
#include <memory>

class NFA {
private:
  std::shared_ptr<State> _startState;
  std::list<std::shared_ptr<State>> _endStates;

public:
  NFA();
  NFA(char);
  NFA(std::shared_ptr<State>, std::list<std::shared_ptr<State>>);

  std::shared_ptr<State> startState();
  std::list<std::shared_ptr<State>> endStates();
  void addNewState(std::shared_ptr<State>);
  void connectNewNFA(NFA);
};

#endif
