# Artefact kind chosen at scaffold time: executable | static | shared
set(@PROJECT_UPPER@_KIND "@ARTIFACT_KIND@")

# The code always lives in a "core" library so the tests can link it, even
# when the shipped artefact is an executable.
if(@PROJECT_UPPER@_KIND STREQUAL "shared")
  set(_core_type SHARED)
else()
  set(_core_type STATIC)
endif()

add_library(@PROJECT_SLUG@_core ${_core_type} @PROJECT_SLUG@.cpp)
add_library(@PROJECT_SLUG@::core ALIAS @PROJECT_SLUG@_core)

target_include_directories(@PROJECT_SLUG@_core PUBLIC
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

target_compile_definitions(@PROJECT_SLUG@_core PRIVATE
  @PROJECT_UPPER@_VERSION="${PROJECT_VERSION}")

target_compile_options(@PROJECT_SLUG@_core PRIVATE -Wall -Wextra -Wpedantic)

if(@PROJECT_UPPER@_KIND STREQUAL "executable")
  add_executable(@PROJECT_SLUG@ main.cpp)
  target_link_libraries(@PROJECT_SLUG@ PRIVATE @PROJECT_SLUG@::core)
  target_compile_options(@PROJECT_SLUG@ PRIVATE -Wall -Wextra -Wpedantic)

  install(TARGETS @PROJECT_SLUG@
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
else()
  set_target_properties(@PROJECT_SLUG@_core PROPERTIES
    OUTPUT_NAME @PROJECT_SLUG@
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR})

  install(TARGETS @PROJECT_SLUG@_core
    EXPORT @PROJECT_SLUG@Targets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
  install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
  install(EXPORT @PROJECT_SLUG@Targets
    NAMESPACE @PROJECT_SLUG@::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/@PROJECT_SLUG@)
endif()
