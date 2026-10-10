# Building @PROJECT_NAME@

## Dependencies

| Dependency | Needed for | Install |
|---|---|---|
| CMake >= 3.16 | build | `sudo apt install cmake` |
| C++ compiler with C++@CXX_STANDARD@ | build | `sudo apt install g++` |
| GoogleTest | tests (optional) | `sudo apt install libgtest-dev` |
| clang-format, clang-tidy | lint (optional) | `sudo apt install clang-format clang-tidy` |

TODO: add the project-specific dependencies from the agreed plan, each with
its install command.

## Host build

```sh
cmake -S . -B build
cmake --build build -j
ctest --test-dir build --output-on-failure
```

If GoogleTest is not installed, configure prints
`GTest not found or BUILD_TESTING=OFF - tests disabled` and the build still
succeeds.

## Cross build

```sh
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=cmake/@TARGET_ARCH@-cross.cmake
cmake --build build -j
```

The toolchain file points at the compiler prefix and sysroot chosen when this
project was created; edit `cmake/@TARGET_ARCH@-cross.cmake` if they move.

## Yocto

The same source tree is what the Yocto recipe builds (`inherit cmake`). The
build never fetches anything at configure time and installs through
`GNUInstallDirs`, so no recipe-side patch is needed.
