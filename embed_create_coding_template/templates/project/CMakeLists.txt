cmake_minimum_required(VERSION 3.16)

project(@PROJECT_NAME@ VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD @CXX_STANDARD@)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# clang-tidy reads compile_commands.json from the build directory.
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

include(GNUInstallDirs)

option(BUILD_TESTING "Build the unit tests" ON)

add_subdirectory(src)

# Vendored third-party source. Never fetched at configure time: a Yocto
# do_configure runs without network access.
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/subprojects/CMakeLists.txt")
  add_subdirectory(subprojects)
endif()

# Tests are optional: a missing GTest must not break the build (Yocto images
# do not ship it unless the recipe asks for it).
find_package(GTest QUIET)
if(BUILD_TESTING AND GTest_FOUND)
  include(CTest)
  add_subdirectory(test)
else()
  message(STATUS "GTest not found or BUILD_TESTING=OFF - tests disabled")
endif()
