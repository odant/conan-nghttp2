project(PackageTest CXX C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(Boost REQUIRED system)
find_package(OpenSSL REQUIRED)

enable_testing()

file(COPY selfsigned.crt selfsigned.key index.html DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/bin)

add_executable(server server.cpp)
target_link_libraries(server
    CONAN_PKG::nghttp2
    Boost::disable_autolinking
    Boost::system
    OpenSSL::SSL
)
add_test(
    NAME server
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
    COMMAND server
)
