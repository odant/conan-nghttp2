# nghttp2 Conan package manager
# Dmitriy Vetutnev, Odant, 2018


find_path(NGHTTP2_INCLUDE_DIR
    NAMES nghttp2/nghttp2.h
    PATHS ${CONAN_INCLUDE_DIRS_NGHTTP2}
    NO_DEFAULT_PATH
)

find_library(NGHTTP2_LIBRARY
    NAMES nghttp2 nghttp2d nghttp232 nghttp232d nghttp264 nghttp264d
    PATHS ${CONAN_LIB_DIRS_NGHTTP2}
    NO_DEFAULT_PATH
)


if(NGHTTP2_INCLUDE_DIR AND EXISTS ${NGHTTP2_INCLUDE_DIR}/nghttp2/nghttp2ver.h)

    file(STRINGS ${NGHTTP2_INCLUDE_DIR}/nghttp2/nghttp2ver.h DEFINE_NGHTTP2_VERSION REGEX "^#define NGHTTP2_VERSION \"[^\"]*\"$")

    string(REGEX REPLACE "^.*NGHTTP2_VERSION \"([0-9]+).*$" "\\1" NGHTTP2_VERSION_MAJOR "${DEFINE_NGHTTP2_VERSION}")
    string(REGEX REPLACE "^.*NGHTTP2_VERSION \"[0-9]+\\.([0-9]+).*$" "\\1" NGHTTP2_VERSION_MINOR "${DEFINE_NGHTTP2_VERSION}")
    string(REGEX REPLACE "^.*NGHTTP2_VERSION \"[0-9]+\\.[0-9]+\\.([0-9]+).*$" "\\1" NGHTTP2_VERSION_PATCH "${DEFINE_NGHTTP2_VERSION}")
    set(NGHTTP2_VERSION_STRING "${NGHTTP2_VERSION_MAJOR}.${NGHTTP2_VERSION_MINOR}.${NGHTTP2_VERSION_PATCH}")

endif()


include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(NGHTTP2
    REQUIRED_VARS NGHTTP2_LIBRARY NGHTTP2_INCLUDE_DIR
    VERSION_VAR NGHTTP2_VERSION_STRING
)


if(NGHTTP2_FOUND)

    set(NGHTTP2_INCLUDE_DIRS ${NGHTTP2_INCLUDE_DIR})
    set(NGHTTP2_LIBRARIES ${NGHTTP2_LIBRARY})
    mark_as_advanced(NGHTTP2_INCLUDE_DIR NGHTTP2_LIBRARY)
    set(NGHTTP2_DEFINITIONS ${CONAN_COMPILE_DEFINITIONS_NGHTTP2}) # Add defines from package_info

    if(NOT TARGET NGHTTP2::nghttp2)

        add_library(NGHTTP2::nghttp2 UNKNOWN IMPORTED)
        set_target_properties(NGHTTP2::nghttp2 PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES ${NGHTTP2_INCLUDE_DIR}
            IMPORTED_LOCATION ${NGHTTP2_LIBRARY}
        )
        if (NGHTTP2_DEFINITIONS)
            set_property(TARGET NGHTTP2::nghttp2
                APPEND PROPERTY INTERFACE_COMPILE_DEFINITIONS ${NGHTTP2_DEFINITIONS}
            )
        endif()

    endif()

    set(_enable_asio)
    foreach(_item ${${CMAKE_FIND_PACKAGE_NAME}_FIND_COMPONENTS})
        if(${_item} STREQUAL asio)
            set(_enable_asio ON)
        endif()
    endforeach()
    unset(_item)

    if(_enable_asio)

        find_library(NGHTTP2_ASIO_LIBRARY
            NAMES nghttp2_asio nghttp2_asiod nghttp2_asio32 nghttp2_asio32d nghttp2_asio64 nghttp2_asio64d
            PATHS ${CONAN_LIB_DIRS_NGHTTP2}
            NO_DEFAULT_PATH
        )

        set(NGHTTP2_ASIO_FIND_REQUIRED ON)
        find_package_handle_standard_args(NGHTTP2_ASIO
            REQUIRED_VARS NGHTTP2_ASIO_LIBRARY
        )

        if(NGHTTP2_ASIO_FOUND)

            set(NGHTTP2_LIBRARIES ${NGHTTP2_ASIO_LIBRARY} ${NGHTTP2_LIBRARIES})
            mark_as_advanced(NGHTTP2_ASIO_LIBRARY)

            if(NOT TARGET NGHTTP2::asio)

                add_library(NGHTTP2::asio UNKNOWN IMPORTED)
                set_target_properties(NGHTTP2::asio PROPERTIES
                    IMPORTED_LOCATION ${NGHTTP2_ASIO_LIBRARY}
                    INTERFACE_LINK_LIBRARIES NGHTTP2::nghttp2
                )

                if(TARGET Boost::system)
                    set_property(TARGET NGHTTP2::asio
                        APPEND PROPERTY INTERFACE_LINK_LIBRARIES Boost::system
                    )
                endif()

                if(TARGET OpenSSL::SSL)
                    set_property(TARGET NGHTTP2::asio
                        APPEND PROPERTY INTERFACE_LINK_LIBRARIES OpenSSL::SSL
                    )
                endif()

            endif()

        endif()

    endif()
    unset(_enable_asio)

endif()

