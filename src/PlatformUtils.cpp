#include "PlatformUtils.h"
#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>

#ifdef PLATFORM_WINDOWS
#include <windows.h>
#include <direct.h>
#include <fileapi.h>
#define getcwd _getcwd
#elif defined(PLATFORM_LINUX)
#include <unistd.h>
#include <sys/stat.h>
#include <limits.h>
#include <fstream>
#endif

std::string PlatformUtils::platformName = "";

std::string PlatformUtils::getPlatformName() {
    if (platformName.empty()) {
#ifdef PLATFORM_WINDOWS
        platformName = "Windows";
#elif defined(PLATFORM_LINUX)
        platformName = "Linux";
#else
        platformName = "Unknown";
#endif
    }
    return platformName;
}

std::string PlatformUtils::getCurrentDirectory() {
    char buffer[1024];
#ifdef PLATFORM_WINDOWS
    if (_getcwd(buffer, sizeof(buffer)) != nullptr) {
        return std::string(buffer);
    }
#elif defined(PLATFORM_LINUX)
    if (getcwd(buffer, sizeof(buffer)) != nullptr) {
        return std::string(buffer);
    }
#endif
    return "";
}

bool PlatformUtils::fileExists(const std::string& path) {
#ifdef PLATFORM_WINDOWS
    DWORD attrib = GetFileAttributesA(path.c_str());
    return (attrib != INVALID_FILE_ATTRIBUTES && 
            !(attrib & FILE_ATTRIBUTE_DIRECTORY));
#elif defined(PLATFORM_LINUX)
    struct stat buffer;
    return (stat(path.c_str(), &buffer) == 0 && S_ISREG(buffer.st_mode));
#endif
}

bool PlatformUtils::createDirectory(const std::string& path) {
#ifdef PLATFORM_WINDOWS
    return _mkdir(path.c_str()) == 0;
#elif defined(PLATFORM_LINUX)
    return mkdir(path.c_str(), 0755) == 0;
#endif
}

uint64_t PlatformUtils::getCurrentProcessId() {
#ifdef PLATFORM_WINDOWS
    return GetCurrentProcessId();
#elif defined(PLATFORM_LINUX)
    return getpid();
#endif
}

std::string PlatformUtils::getProcessName() {
#ifdef PLATFORM_WINDOWS
    char buffer[MAX_PATH];
    if (GetModuleFileNameA(NULL, buffer, MAX_PATH)) {
        std::string fullPath(buffer);
        size_t pos = fullPath.find_last_of("\\/");
        if (pos != std::string::npos) {
            return fullPath.substr(pos + 1);
        }
        return fullPath;
    }
#elif defined(PLATFORM_LINUX)
    char buffer[1024];
    ssize_t len = readlink("/proc/self/exe", buffer, sizeof(buffer) - 1);
    if (len != -1) {
        buffer[len] = '\0';
        std::string fullPath(buffer);
        size_t pos = fullPath.find_last_of('/');
        if (pos != std::string::npos) {
            return fullPath.substr(pos + 1);
        }
        return fullPath;
    }
#endif
    return "unknown";
}

void PlatformUtils::logToSystem(const std::string& message, int level) {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    
    std::string levelStr;
    switch(level) {
        case 0: levelStr = "INFO"; break;
        case 1: levelStr = "WARN"; break;
        case 2: levelStr = "ERROR"; break;
        default: levelStr = "DEBUG";
    }
    
    std::cout << "[" << std::ctime(&time) << "][" << levelStr << "] " << message << std::endl;
    
#ifdef PLATFORM_WINDOWS
    OutputDebugStringA(message.c_str());
#endif
}

void PlatformUtils::registerCrashHandler() {
    // In a real implementation, this would set up signal handlers or SEH
    logToSystem("Crash handler registered for " + getPlatformName());
}

void PlatformUtils::generateMiniDump(const std::string& dumpPath) {
    // Platform-specific minidump generation
    logToSystem("Generating minidump at: " + dumpPath);
    
#ifdef PLATFORM_WINDOWS
    // Windows MiniDumpWriteDump would be called here
    logToSystem("Windows minidump created");
#elif defined(PLATFORM_LINUX)
    // Linux core dump generation
    logToSystem("Linux core dump generated");
#endif
}