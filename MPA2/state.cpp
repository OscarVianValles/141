#include "state.hpp"
#include <iostream>

// Constructor
State::State(char allowableCharacter) {
  _type = getType(allowableCharacter);
  _allowableCharacter = allowableCharacter;
}

// Simply add a new state to the list of existing states
void State::addState(std::shared_ptr<State> newState) {
  _nextStates.push_back(newState);
}

std::list<std::shared_ptr<State>> State::check(char testChar) {
  // If the test character is in the array of allowable characters, the next
  // states will be returned
  if (_type == _union || _type == _empty) {
    return _nextStates;
  }

  if (testChar == _allowableCharacter) {

    std::cout << "Allowable: " << _allowableCharacter
              << " TestChar:  " << testChar << " 1 " << _nextStates.size()
              << std::endl;
    return _nextStates;
  }

  // Return an empty list if the test character is not in the list of
  // allowable characters
  else {
    std::cout << "Allowable: " << _allowableCharacter
              << " TestChar:  " << testChar << " 0" << std::endl;
    std::list<std::shared_ptr<State>> empty;
    empty.push_front(std::shared_ptr<State>(nullptr));
    return empty;
  }
}

type State::stateType() { return _type; }

std::list<std::shared_ptr<State>> State::nextStates() { return _nextStates; }
