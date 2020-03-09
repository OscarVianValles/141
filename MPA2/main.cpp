#include "in2post.hpp"
#include "regex.hpp"
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>

int main() {
  std::ofstream output("valles.out");
  std::ifstream input("mpa3.in");

  std::string lines;
  // Opening file
  if (input.is_open()) {
    // Creating buffer string
    std::string lines;
    // Create counters
    int testCasesSize = -1;
    int testCaseLength = 0;
    // Create persistent regex for loop
    Regex regex("a");
    while (getline(input, lines)) {
      lines.erase(std::remove(lines.begin(), lines.end(), '\r'), lines.end());
      // Get the number of testCases
      if (testCasesSize == -1) {
        testCasesSize = std::stoi(lines) + 1;
      } else if (testCasesSize > 0) {
        // Create regex if testCaseLength is not yet set or a new testcase was
        // created
        if (testCaseLength == 0) {
          regex = Regex(in2post(lines));
          // Reduce testCaseSize when lenght becomes 0
          --testCasesSize;
          // Change testCaseLength to -1 to know that the regex was already
          // created
          --testCaseLength;
        } else if (testCaseLength == -1) {
          testCaseLength = std::stoi(lines);
        } else if (testCaseLength > 0) {
          output << (regex.match(lines) ? "yes" : "no") << std::endl;
          std::cout << (regex.match(lines) ? "yes" : "no") << std::endl;
          --testCaseLength;
        }
      }
    }
  }

  return 0;
}
