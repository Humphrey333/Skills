# @PROJECT_NAME@

TODO: what this project is and how it works (from the agreed plan).

## Layout

| Path | Purpose |
|---|---|
| `CMakeLists.txt` | top-level build; each subfolder has its own |
| `src/` | source code |
| `include/` | public headers |
| `test/` | GoogleTest unit tests (optional, skipped if GTest is absent) |
| `cmake/` | toolchain files |
| `subprojects/` | vendored third-party source |
| `tools/` | debug, release and flash helper scripts |
| `docs/` | design notes and GitHub templates |
| `build/` | build output (git-ignored) |

See [BUILD.md](BUILD.md) for dependencies and build instructions.
