project(tst_nghttp2 CXX C)
cmake_minimum_required(VERSION 3.4)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

message(STATUS "CMAKE_MODULE_PATH => ${CMAKE_MODULE_PATH}")

set(OPENSSL_ROOT_DIR ${CONAN_OPENSSL_ROOT})

set(Boost_USE_STATIC_LIBS ON)
set(Boost_NO_SYSTEM_PATHS ON)
set(BOOST_ROOT ${CONAN_BOOST_HEADERS_ROOT})
set(BOOST_INCLUDEDIR ${CONAN_INCLUDE_DIRS_BOOST_HEADERS})
set(BOOST_LIBRARYDIR ${CONAN_LIB_DIRS_BOOST_LIBRARIES})

option(ENABLE_ASIO_LIB "Build C++ libnghttp2_asio library" ON)
option(ENABLE_APP "Build applications (nghttp, nghttpd, nghttpx and h2load)" OFF)
option(ENABLE_EXAMPLES "Build examples" OFF)
option(ENABLE_PYTHON_BINDINGS "Build Python bindings" OFF)
option(WITH_LIBXML2 "Use libxml2" OFF)
option(WITH_SPDYLAY "Use spdylay" OFF)
option(WITH_MRUBY "Use mruby" OFF)
option(WITH_NEVERBLEED "Use neverbleed" OFF)

if(WIN32)
    set(CMAKE_DEBUG_POSTFIX "d")
    add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
    add_definitions(-D_CRT_NONSTDC_NO_DEPRECATE)
endif()

add_subdirectory(src)

file(
    GLOB_RECURSE PROJECT_FILES FOLLOW_SYMLINKS
    *.txt *.c *.cpp *.hpp *.h *.in *.cmake *.sh *.md
    README* AUTHORS* LICENSE*
    .travis.yml
)

