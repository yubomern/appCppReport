cmake_minimum_required(VERSION 3.16)
project(CrashDumpAnalyzer VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Platform detection
if(WIN32)
    add_compile_definitions(PLATFORM_WINDOWS)
    add_compile_options(/W4 /O2 /EHsc)
    set(PLATFORM_LIBS dbghelp.lib)
elseif(UNIX)
    add_compile_definitions(PLATFORM_LINUX)
    add_compile_options(-Wall -Wextra -O2 -g)
    set(PLATFORM_LIBS dl pthread)
endif()

# Set output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Source files
set(SOURCES
    src/main.cpp
    src/CoreDumpManager.cpp
    src/CoreDumpData.cpp
    src/SystemMetrics.cpp
    src/CrashAnalysis.cpp
    src/PlatformUtils.cpp
    src/JsonCrashExporter.cpp
    src/CsvCrashExporter.cpp
    src/CrashExporterFactory.cpp
)

set(HEADERS
    src/CoreDumpManager.h
    src/CoreDumpData.h
    src/SystemMetrics.h
    src/CrashAnalysis.h
    src/PlatformUtils.h
    src/ICrashExporter.h
    src/JsonCrashExporter.h
    src/CsvCrashExporter.h
    src/CrashExporterFactory.h
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE src)

# Link libraries
target_link_libraries(${PROJECT_NAME} ${PLATFORM_LIBS})

# Platform-specific settings
if(WIN32)
    # Disable console window for release builds (optional)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        LINK_FLAGS "/SUBSYSTEM:CONSOLE"
    )
endif()

# Print configuration
message(STATUS "Building for: ${CMAKE_SYSTEM_NAME}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")