#include "regex.hpp"
#include "type.hpp"
#include <iostream>

Regex::Regex(std::string inputRegex) { _regex = _createNFA(inputRegex); }

bool Regex::match(std::string testString) {
  // Create stack
  std::stack<std::shared_ptr<State>> stateStack;
  std::stack<std::string> stringStack;

  // Create temporary variables for loop
  std::shared_ptr<State> currState(nullptr);
  std::string currString;
  std::list<std::shared_ptr<State>> nextStates;

  // Check the states
  stateStack.push(_regex.startState());
  stringStack.push(testString);
  while (!stateStack.empty()) {
    // Get the current states
    currState = stateStack.top();
    currString = stringStack.top();
    stateStack.pop();
    stringStack.pop();

    // Get the next states depending on the next string.
    if (currString != "e") {
      nextStates = currState->check(currString[0]);
    } else {
      // Handle if empty string is passed. This is true when the current state
      // is empty and the next state is not empty
      if (currState->stateType() == _empty && currState->nextStates().empty() &&
          currString == "e") {
        std::cout << "here" << std::endl;
        return true;
      } else {
        return false;
      }
    }

    // If the content of the next state is a nullptr, that means the check has
    // failed and to remove this state from the stack
    if (nextStates.front() == nullptr && nextStates.size() != 0) {
      continue;
    }

    // If there are no more next states and the current string is empty, that
    // means that the regex is successful
    if (nextStates.size() == 0 && currString.substr(1).empty()) {
      return true;
    }

    while (!nextStates.empty()) {
      stateStack.push(nextStates.front());
      // If the current state is of type empty or union, do not remove the
      // preceding character
      if (currState->stateType() == _empty ||
          currState->stateType() == _union) {
        stringStack.push(currString);
      } else {
        stringStack.push(currString.substr(1));
      }

      nextStates.pop_front();
    }
  }

  return false;
}

NFA Regex::_createNFA(std::string postFix) {
  while (!postFix.empty()) {
    switch (postFix.front()) {
    case 'a':
    case 'b':
    case 'e': {
      _nfaStack.push(NFA(postFix.front()));
      break;
    }
    case 'U': {
      // Store the start states and end states of the 2 previous NFAs
      std::list<std::shared_ptr<State>> startStates;
      std::list<std::shared_ptr<State>> endStates;
      for (int i = 0; i < 2; ++i) {
        startStates.push_back(_nfaStack.top().startState());
        for (auto state : _nfaStack.top().endStates()) {
          endStates.push_back(state);
        }
        _nfaStack.pop();
      }

      // A new union state is createwd
      auto unionState = std::make_shared<State>('U');

      // The start state of all previous states will then be the end state of
      // the new state.
      for (auto state : startStates) {
        unionState->addState(state);
      }

      // A new NFA is created with the union as the start state and the end
      // states of the 2 previous NFAs
      _nfaStack.push(NFA(unionState, endStates));
      break;
    }
    case 'O': {
      NFA next = _nfaStack.top();
      _nfaStack.pop();
      NFA prev = _nfaStack.top();
      _nfaStack.pop();
      prev.addNewState(next.startState());

      if (next.endStates().size() == 0) {
        _nfaStack.push(NFA(prev.startState(), prev.endStates()));
      } else {
        _nfaStack.push(NFA(prev.startState(), next.endStates()));
      }
      break;
    }

    default:
      throw - 1;
    }

    postFix = postFix.substr(1);
  }

  if (_nfaStack.size() == 1) {
    return _nfaStack.top();
  } else {
    throw - 1;
  }
}
