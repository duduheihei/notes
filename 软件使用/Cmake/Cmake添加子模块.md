```cmake
set(CURRENT_INC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/")
set(CURRENT_LIB_DIR "${CMAKE_CURRENT_SOURCE_DIR}/")
if(CMAKE_SYSTEM_NAME MATCHES "Windows")
    add_library(test_func STATIC IMPORTED GLOBAL)
    set_target_properties(test_func PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${CURRENT_INC_DIR}/inc"	
		IMPORTED_LOCATION_DEBUG "${CURRENT_LIB_DIR}/lib/vs2019_x64/test_func_d.lib"
        IMPORTED_LOCATION_RELEASE "${CURRENT_LIB_DIR}/lib/vs2019_x64/test_func.lib"
        IMPORTED_LOCATION_MINSIZEREL "${CURRENT_LIB_DIR}/lib/vs2019_x64/test_func.lib"
        IMPORTED_LOCATION_RELWITHDEBINFO "${CURRENT_LIB_DIR}/lib/vs2019_x64/test_func.lib"
        VERSION 1.0.0.1
    )
else() # tda4
    add_library(test_func STATIC IMPORTED GLOBAL)
    set_target_properties(test_func PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${CURRENT_INC_DIR}/inc"
        IMPORTED_LOCATION "${CURRENT_LIB_DIR}/lib/andriod/libtest_func.a"
        VERSION 1.0.0.1
    )
endif()

target_link_libraries(test_func INTERFACE
    dep_liba
    dep_libb
)

```