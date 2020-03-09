#include "nfa.hpp"
#include <iostream>

NFA::NFA() {}

NFA::NFA(char startChar) {
  _startState = new State(startChar);
  std::list<State *> endStates;
  endStates.push_back(_startState);
  _endStates = endStates;
}

NFA::NFA(State *startState, std::list<State *> endStates) {
  _startState = startState;
  _endStates = endStates;
}

NFA::NFA(State *startState) { _startState = startState; }

void NFA::addNewState(State *newState) {
  for (auto state : _endStates) {
    state->addState(newState);
  }
}
void NFA::connectNewNFA(NFA newNFA) {
  for (auto state : newNFA._endStates) {
    addNewState(state);
  }
}

State *NFA::startState() { return _startState; }
std::list<State *> NFA::endStates() { return _endStates; }
