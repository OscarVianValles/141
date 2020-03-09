#include "nfa.hpp"
#include <iostream>
#include <memory>

NFA::NFA() {}

NFA::NFA(char startChar) {
  _startState = std::make_shared<State>(startChar);
  std::list<std::shared_ptr<State>> endStates;
  endStates.push_back(_startState);
  _endStates = endStates;
}

NFA::NFA(std::shared_ptr<State> startState,
         std::list<std::shared_ptr<State>> endStates) {
  _startState = startState;
  _endStates = endStates;
}

void NFA::addNewState(std::shared_ptr<State> newState) {
  for (auto state : _endStates) {
    state->addState(newState);
  }
}

void NFA::connectNewNFA(NFA newNFA) {
  for (auto state : newNFA._endStates) {
    addNewState(state);
  }
}

std::shared_ptr<State> NFA::startState() { return _startState; }

std::list<std::shared_ptr<State>> NFA::endStates() { return _endStates; }
