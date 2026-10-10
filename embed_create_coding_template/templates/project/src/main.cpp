#include <iostream>

#include "@PROJECT_SLUG@/@PROJECT_SLUG@.hpp"

int main() {
  std::cout << "@PROJECT_NAME@ " << @PROJECT_SLUG@::version() << '\n';
  return 0;
}
