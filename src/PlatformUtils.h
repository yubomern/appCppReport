#pragma once
#include <string>
#include <cstdint>

class PlatformUtils {
public:
    // Association: CoreDumpManager uses PlatformUtils
    
    static std::string getPlatformName();
    static std::string getCurrentDirectory();
    static bool fileExists(const std::string& path);
    static bool createDirectory(const std::string& path);
    static uint64_t getCurrentProcessId();
    static std::string getProcessName();
    static void logToSystem(const std::string& message, int level = 0);
    
    // Platform-specific crash handling
    static void registerCrashHandler();
    static void generateMiniDump(const std::string& dumpPath);
    
private:
    static std::string platformName;
};