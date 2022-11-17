# set the project name and version
project(iotG4)

message("Compiling....")

# add the executable
add_executable(sensores "ESP32/sensores.c")

target_link_libraries(sensores PRIVATE m)