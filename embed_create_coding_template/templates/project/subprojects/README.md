# subprojects

Vendored third-party source used by this project. Each subdirectory that has
its own `CMakeLists.txt` is added to the build automatically.

Add a dependency by placing its source here (copy or git submodule). Do **not**
fetch it from CMake (`FetchContent`/`ExternalProject`): the Yocto build runs
`do_configure` without network access, so every dependency must already be on
disk or provided by the recipe.
