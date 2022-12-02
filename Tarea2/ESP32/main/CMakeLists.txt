if(${IDF_TARGET} STREQUAL "linux")
    set(requires esp_stubs)
endif()



idf_component_register(SRCS "main.c" 
                        INCLUDE_DIRS "."
                        REQUIRES ${requires})
set(COMPONENT_SRCS "main.c" "../components/conexion/udp.c")
set(COMPONENT_ADD_INCLUDEDIRS "" "../components/")