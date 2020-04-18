cmake_minimum_required(VERSION 3.10)

# set the project name
project(plxr VERSION 0.5)

set(CMAKE_BUILD_TYPE Release)


add_library(plxr SHARED src/plxr.cxx)
install(TARGETS plxr DESTINATION /usr/lib)



