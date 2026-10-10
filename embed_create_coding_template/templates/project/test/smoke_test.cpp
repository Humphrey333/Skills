#include <gtest/gtest.h>

#include "@PROJECT_SLUG@/@PROJECT_SLUG@.hpp"

TEST(Smoke, VersionIsReported) {
  EXPECT_FALSE(@PROJECT_SLUG@::version().empty());
}
