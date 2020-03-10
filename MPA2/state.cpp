#include "state.hpp"
#include "type.hpp"
#include <iostream>

// Constructor
State::State(char allowableCharacter) {
  _type = getType(allowableCharacter);
  if (_type == _union) {
    _allowableCharacter = 'e';
  } else {
    _allowableCharacter = allowableCharacter;
  }
}

// Simply add a new state to the list of existing states
void State::addState(std::shared_ptr<State> newState) {
  _nextStates.push_back(newState);
}

std::list<std::shared_ptr<State>> State::check(char testChar) {

  // If the test character is in the array of allowable characters, the next
  // states will be returned
  if (testChar == _allowableCharacter) {

    std::cout << "T Allowable: " << _allowableCharacter
              << " TestChar: " << testChar << " " << _nextStates.size() << " "
              << _type << " " << this << std::endl;
    return _nextStates;
  }

  // Return an list with an invalid state if the test character is not in the
  // list of allowable characters
  else {
    std::cout << "F Allowable: " << _allowableCharacter
              << " TestChar: " << testChar << " " << _nextStates.size() << " "
              << _type << " " << std::endl;
    std::list<std::shared_ptr<State>> empty;
    auto invalidState = std::make_shared<State>('x');
    empty.push_front(invalidState);
    return empty;
  }
}

type State::stateType() { return _type; }

std::list<std::shared_ptr<State>> State::nextStates() { return _nextStates; }
