add_executable(@PROJECT_SLUG@_tests smoke_test.cpp)

target_link_libraries(@PROJECT_SLUG@_tests PRIVATE
  @PROJECT_SLUG@::core
  GTest::gtest_main)

add_test(NAME smoke COMMAND @PROJECT_SLUG@_tests)
