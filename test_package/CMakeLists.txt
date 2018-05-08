# Test for nghttp2 Conan package
# Dmitriy Vetutnev, Odant, 2018


project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)


include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)


enable_testing()


file(COPY selfsigned.crt selfsigned.key index.html DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/bin)


# Conan imported targets
add_executable(test_server_CONAN_PKG test_server.cpp)
target_link_libraries(test_server_CONAN_PKG CONAN_PKG::nghttp2)
set_target_properties(test_server_CONAN_PKG
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_server_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
    COMMAND test_server_CONAN_PKG
)


# Common imported targets
find_package(Threads REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
find_package(OpenSSL REQUIRED)
find_package(NGHTTP2 REQUIRED COMPONENTS asio)

add_executable(test_server test_server.cpp)
target_link_libraries(test_server NGHTTP2::asio Threads::Threads)
set_target_properties(test_server
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_server
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
    COMMAND test_server
)
