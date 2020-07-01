cmake_minimum_required(VERSION 3.16.2)

# Download and unpack googletest at configure time
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()
execute_process(COMMAND ${CMAKE_COMMAND} --build .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

# Prevent overriding the parent project's compiler/linker
# settings on Windows
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Add googletest directly to our build. This defines
# the gtest and gtest_main targets.
add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/googletest-src
                 ${CMAKE_CURRENT_BINARY_DIR}/googletest-build
                 EXCLUDE_FROM_ALL)

# The gtest/gtest_main targets carry header search path
# dependencies automatically when using CMake 2.8.11 or
# later. Otherwise we have to add them here ourselves.
if (CMAKE_VERSION VERSION_LESS 2.8.11)
  include_directories("${gtest_SOURCE_DIR}/include")
endif()


#project(plxr LANGUAGES C CXX VERSION 0.5)
project(plxr VERSION 0.5)
enable_testing()
include(CTest)
set(CMAKE_BUILD_TYPE Release)
find_package(ADIOS2 REQUIRED)
add_library(plxr SHARED src/plxr.cxx)
target_link_libraries(plxr adios2::cxx11_mpi  MPI::MPI_C)
install(TARGETS plxr DESTINATION /usr/lib)

# Now simply link against gtest or gtest_main as needed. Eg
add_executable(test_write_read test/test_write_read.cxx)
target_link_libraries(test_write_read gtest_main plxr)
target_include_directories(test_write_read PUBLIC src)
add_test(NAME write_read_test COMMAND test_write_read)

