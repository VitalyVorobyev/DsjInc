cmake_minimum_required (VERSION 3.1)
project (libDsjData)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_BUILD_TYPE Release)

set(PROJECT_LINK_LIBS libRecoObj.so)
link_directories(/home/vitaly/work/MyLibs/libReco/build/)

find_package(ROOT REQUIRED)

file(GLOB SOURCES dataobj/*.cc)

add_library(dsjdata SHARED ${SOURCES})
target_link_libraries(dsjdata ${PROJECT_LINK_LIBS})

install(TARGETS dsjdata DESTINATION /usr/lib)

