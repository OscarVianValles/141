#include "in2post.hpp"
#include "type.hpp"
#include <iostream>

// Specific concatenation operator is added so that it will be easier later on
// to identify precedence when converting to postfix notation
std::string addConcat(std::string inputString) {
  int inLen = inputString.length();
  std::string output;

  type token = _invalid, prevToken = _invalid;
  for (int i = 0; i < inLen; ++i) {
    token = getType(inputString[i]);
    // Skip if token or prevToken is a space or other invalid tokens
    if (token == _invalid || prevToken == _invalid) {
      // However, if token is valid, it will be added to the output
      if (token != _invalid) {
        output.push_back(inputString[i]);
      }

      // Properly set prevToken so that the loop will continue properly
      prevToken = token;
      continue;
    }

    // Based on the rules of concatenation, the tokens that can be concatenated
    // to are the elements of the alphabet and the open parenthesis. This is the
    // purpose of the first check. The tokens that can concatenate are the
    // elements of the alphabet aOb, the kleene star a*b, and the close
    // parenthesis (a)*a. This is checked in the second statement.
    //
    // Another thing added here is checking for empty and adding the appropriate
    // concatenation. This is so that ea will become eOa, ae will become aOe
    if ((token == _alpha || token == _open || token == _empty) &&
        (prevToken == _alpha || prevToken == _kleene || prevToken == _close ||
         prevToken == _empty)) {
      output.push_back('O');
    }

    // The token is then added to the output
    output.push_back(inputString[i]);
    // Set prevToken to previous token
    prevToken = token;
  }

  return output;
}

// Converts infix regex to postfix regex using the Shunting-yard algorithm
// Source: https://en.wikipedia.org/wiki/Shunting-yard_algorithm
std::string in2post(std::string inputString) {

  // Add Specific Concat Operator and remove spaces
  inputString = addConcat(inputString);

  // Setup needed components of the Shunting-yard algorithm
  std::string output;
  std::stack<type> op;
  int inLen = inputString.length();

  for (int i = 0; i < inLen; ++i) {
    // get Token Type
    auto token = getType(inputString[i]);
    // If it is an element of the alphabet or empty string, it will be added to
    // the output, then it moves on to the next loop
    if (token == _alpha || token == _empty) {
      output.push_back(inputString[i]);
    }

    // Algo to perform if it is an operator
    else if (token == _concat || token == _union || token == _kleene) {
      // The loop pops all elements of the stack until the top of the stack is
      // an open parenthesis or the next operator is of lower precedence
      while (!op.empty()) {
        if (op.top() != _open && op.top() >= token) {
          output.push_back(getChar(op.top()));
          op.pop();
        } else {
          break;
        }
      }
      op.push(token);
    }

    // If it is an open parenthesis, simply push the token to the stack
    else if (token == _open) {
      op.push(token);
    }

    // If it is a close parenthesis, pop all elements of the stack until an open
    // parenthesis is found. Finally, pop the open parenthesis
    else if (token == _close) {
      while (!op.empty()) {
        if (op.top() != _open) {
          output.push_back(getChar(op.top()));
          op.pop();
        } else {
          break;
        }
      }
      if (!op.empty() && op.top() == _open) {
        op.pop();
      }
    }
  }

  // Place all operators still on the stack back to the output
  while (!op.empty()) {
    output.push_back(getChar(op.top()));
    op.pop();
  }

  return output;
}
