# The following lines of boilerplate have to be in your project's
# CMakeLists in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.16)

message("IDF TARGET: ${IDF_TARGET}")
message("IDF PATH: $ENV{IDF_PATH}")
message("XTENSA PATH: $ENV{xtensa-esp32-elf}")
message("XTENSA GCC PATH: $ENV{xtensa-esp32-elf-gcc}")
set(xtensa-esp32-elf-gcc "/home/malva/.espressif/tools/xtensa-esp32-elf/esp-2022r1-11.2.0/xtensa-esp32-elf/bin/xtensa-esp32-elf-gcc")

if("${IDF_TARGET}" STREQUAL "linux")
    message("IDF TARGET is Linux")
    list(APPEND EXTRA_COMPONENT_DIRS "$ENV{IDF_PATH}/tools/mocks/freertos/")
    set(COMPONENTS main)
    include($ENV{IDF_PATH}/tools/cmake/project.cmake)
else()
    message("IDF TARGET is not Linux")
    set(EXTRA_COMPONENT_DIRS $ENV{IDF_PATH}/examples/common_components/protocol_examples_common)
    include($ENV{IDF_PATH}/tools/cmake/project.cmake)
endif()

project(tcp_client)
