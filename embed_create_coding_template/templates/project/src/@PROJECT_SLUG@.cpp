#include "@PROJECT_SLUG@/@PROJECT_SLUG@.hpp"

namespace @PROJECT_SLUG@ {

std::string_view version() noexcept {
  // Injected by src/CMakeLists.txt so the CMake project version is the single
  // source of truth.
  return @PROJECT_UPPER@_VERSION;
}

}  // namespace @PROJECT_SLUG@
