# nghttp2 Conan package
# Dmitriy Vetutnev, Odant, 2018


project(conan_nghttp2 CXX C)
cmake_minimum_required(VERSION 3.4)


set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)


option(ENABLE_ASIO_LIB "Build C++ libnghttp2_asio library" ON)
option(ENABLE_APP "Build applications (nghttp, nghttpd, nghttpx and h2load)" OFF)
option(ENABLE_EXAMPLES "Build examples" OFF)
option(ENABLE_PYTHON_BINDINGS "Build Python bindings" OFF)
option(WITH_LIBXML2 "Use libxml2" OFF)
option(WITH_SPDYLAY "Use spdylay" OFF)
option(WITH_MRUBY "Use mruby" OFF)
option(WITH_NEVERBLEED "Use neverbleed" OFF)


if(WIN32)

    add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
    add_definitions(-D_CRT_NONSTDC_NO_DEPRECATE)

    # Set binary suffix
    if(${CMAKE_SIZEOF_VOID_P} EQUAL 8)
        set(CMAKE_RELEASE_POSTFIX "64")
        set(CMAKE_RELWITHDEBINFO_POSTFIX "64")
        set(CMAKE_MINSIZEREL_POSTFIX "64")
        set(CMAKE_DEBUG_POSTFIX "64d")
    elseif(${CMAKE_SIZEOF_VOID_P} EQUAL 4)
        #set(CMAKE_RELEASE_POSTFIX "32")
        #set(CMAKE_RELWITHDEBINFO_POSTFIX "32")
        #set(CMAKE_MINSIZEREL_POSTFIX "32")
        #set(CMAKE_DEBUG_POSTFIX "32")
        set(CMAKE_DEBUG_POSTFIX "d")
    else()
        message(FATAL_ERROR "Unknow architecture")
    endif()

endif()


add_subdirectory(src)
