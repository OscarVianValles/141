#ifndef REGEX_H
#define REGEX_H

#include "nfa.hpp"
#include "state.hpp"
#include <memory>
#include <stack>
#include <string>

class Regex {
private:
  std::stack<NFA> _nfaStack;
  NFA _regex;

  NFA _createNFA(std::string);

public:
  Regex(std::string);
  bool match(std::string);
};

#endif
