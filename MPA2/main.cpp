#include "in2post.hpp"
#include "regex.hpp"
#include <iostream>

#include <string>
int main() {
  Regex a(in2post("a(aUb)a"));
  std::cout << a.match("aaaa") << std::endl;

  return 0;
}
