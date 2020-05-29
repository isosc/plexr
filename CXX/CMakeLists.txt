cmake_minimum_required(VERSION 3.10)

# set the project name
project(plxr VERSION 0.5)

set(CMAKE_BUILD_TYPE Release)

find_package(ADIOS2 REQUIRED)

add_library(plxr SHARED src/plxr.cxx)
target_link_libraries(plxr PRIVATE adios2)
install(TARGETS plxr DESTINATION /usr/lib)



