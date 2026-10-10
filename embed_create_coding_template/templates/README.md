# Template tree

This directory is the definition of the scaffold that `embed_create_coding_template` writes.
It is skill documentation plus source files; it is **not** copied into generated projects.

- `project/` — copied to `<plan repo root>/<project-name>/`, then specialised.
- `licenses/` — one file is copied to the project's `LICENSE`.
- `ci/` — one file is copied to `.github/workflows/ci.yml` or `.gitlab-ci.yml`, or none.
- `project/cmake/cross-toolchain.cmake.in` — renamed `cmake/<arch>-cross.cmake`; dropped for host-only.

## Placeholders

Substituted mechanically after copying. After substitution, `grep -rn '@[A-Z_]*@'` over the
generated project must return nothing.

| Placeholder | Meaning |
|---|---|
| `@PROJECT_NAME@` | name as the developer typed it |
| `@PROJECT_SLUG@` | lower_snake: filenames, namespace, include subdirectory, targets |
| `@PROJECT_UPPER@` | UPPER_SNAKE: header guard and CMake variable prefixes |
| `@ARTIFACT_KIND@` | `executable`, `static` or `shared` |
| `@CXX_STANDARD@` | e.g. `17` |
| `@TARGET_ARCH@` | e.g. `aarch64` (cross builds only) |
| `@COMPILER_PREFIX@` | e.g. `aarch64-buildroot-linux-gnu` (cross builds only) |
| `@SYSROOT@` | absolute sysroot path (cross builds only) |
| `@YEAR@`, `@COPYRIGHT_HOLDER@` | license header |

Files and directories named with a placeholder (`src/@PROJECT_SLUG@.cpp`,
`include/@PROJECT_SLUG@/`) are renamed, not just edited.

Host-only projects have no `@TARGET_ARCH@` etc., so `BUILD.md`'s "Cross build" section and
`cmake/` are removed together with the toolchain file.
