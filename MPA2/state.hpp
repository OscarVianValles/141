#ifndef STATE_H
#define STATE_H

#include "type.hpp"
#include <list>
#include <memory>
#include <vector>
class State {
private:
  type _type;
  char _allowableCharacter;
  std::list<std::shared_ptr<State>> _nextStates;

public:
  State(char);
  void addState(std::shared_ptr<State>);
  std::list<std::shared_ptr<State>> check(char);

  type stateType();
  std::list<std::shared_ptr<State>> nextStates();
};

#endif
