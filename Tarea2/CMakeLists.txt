# set the project name and version
project(iotG4)

message("Compiling....")

# add the executable
#add_executable(sensores "ESP32/sensores.c")
add_executable(empaquetamiento "ESP32/components/payload/empaquetamiento.c")

#target_link_libraries(sensores PRIVATE m)
target_link_libraries(empaquetamiento PRIVATE m)

target_compile_options(empaquetamiento PRIVATE -Wall -Wextra -Wpedantic -Werror)