/**
 * @file @PROJECT_SLUG@.hpp
 * @brief Public interface of @PROJECT_NAME@.
 */
#ifndef @PROJECT_UPPER@_HPP
#define @PROJECT_UPPER@_HPP

#include <string_view>

namespace @PROJECT_SLUG@ {

/** @brief Returns the project version string, e.g. "0.1.0". */
std::string_view version() noexcept;

}  // namespace @PROJECT_SLUG@

#endif  // @PROJECT_UPPER@_HPP
