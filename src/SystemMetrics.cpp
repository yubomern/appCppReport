#include "SystemMetrics.h"
#include <sstream>
#include <iomanip>

#ifdef PLATFORM_WINDOWS
#include <windows.h>
#include <psapi.h>
#include <processthreadsapi.h>
#elif defined(PLATFORM_LINUX)
#include <unistd.h>
#include <fstream>
#include <sys/sysinfo.h>
#endif

SystemMetrics::SystemMetrics() 
    : memoryUsageMB(0), cpuUsagePercent(0), threadCount(0), processName("unknown") {
    timestamp = std::chrono::system_clock::now();
}

SystemMetrics::SystemMetrics(const std::string& procName)
    : memoryUsageMB(0), cpuUsagePercent(0), threadCount(0), processName(procName) {
    timestamp = std::chrono::system_clock::now();
}

void SystemMetrics::collect() {
    timestamp = std::chrono::system_clock::now();
    
#ifdef PLATFORM_WINDOWS
    HANDLE hProcess = GetCurrentProcess();
    PROCESS_MEMORY_COUNTERS pmc;
    if (GetProcessMemoryInfo(hProcess, &pmc, sizeof(pmc))) {
        memoryUsageMB = pmc.WorkingSetSize / (1024 * 1024);
    }
    
    FILETIME creationTime, exitTime, kernelTime, userTime;
    if (GetProcessTimes(hProcess, &creationTime, &exitTime, &kernelTime, &userTime)) {
        static ULARGE_INTEGER lastKernel, lastUser;
        static ULARGE_INTEGER lastTime;
        
        ULARGE_INTEGER now;
        GetSystemTimeAsFileTime((FILETIME*)&now);
        
        ULARGE_INTEGER kTime, uTime;
        kTime.LowPart = kernelTime.dwLowDateTime;
        kTime.HighPart = kernelTime.dwHighDateTime;
        uTime.LowPart = userTime.dwLowDateTime;
        uTime.HighPart = userTime.dwHighDateTime;
        
        if (lastTime.QuadPart != 0) {
            ULONGLONG totalSys = (kTime.QuadPart - lastKernel.QuadPart) + 
                                 (uTime.QuadPart - lastUser.QuadPart);
            ULONGLONG totalTime = now.QuadPart - lastTime.QuadPart;
            cpuUsagePercent = (totalSys * 100) / totalTime;
        }
        
        lastKernel = kTime;
        lastUser = uTime;
        lastTime = now;
    }
    
    // Get thread count
    DWORD threadCountDWORD = 0;
    if (GetProcessHandleCount(hProcess, &threadCountDWORD)) {
        threadCount = threadCountDWORD;
    }
    
#elif defined(PLATFORM_LINUX)
    // Linux implementation
    std::ifstream statFile("/proc/self/stat");
    if (statFile.is_open()) {
        std::string line;
        std::getline(statFile, line);
        std::istringstream iss(line);
        
        std::string token;
        int fieldNum = 0;
        while (std::getline(iss, token, ' ')) {
            if (fieldNum == 13) {  // utime
                // Parse CPU time
            } else if (fieldNum == 19) {  // num_threads
                threadCount = std::stoull(token);
            }
            fieldNum++;
        }
        statFile.close();
    }
    
    // Memory usage
    std::ifstream memFile("/proc/self/status");
    if (memFile.is_open()) {
        std::string line;
        while (std::getline(memFile, line)) {
            if (line.find("VmRSS:") == 0) {
                std::istringstream iss(line);
                std::string key;
                uint64_t value;
                iss >> key >> value;
                memoryUsageMB = value / 1024;
                break;
            }
        }
        memFile.close();
    }
    
    // CPU usage (simplified)
    struct sysinfo sysInfo;
    if (sysinfo(&sysInfo) == 0) {
        cpuUsagePercent = (sysInfo.loads[0] * 100) / 65536;
    }
#endif
}

std::string SystemMetrics::getTimestamp() const {
    auto time = std::chrono::system_clock::to_time_t(timestamp);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
    return ss.str();
}

std::string SystemMetrics::toJson() const {
    std::stringstream ss;
    ss << "{"
       << "\"timestamp\":\"" << getTimestamp() << "\","
       << "\"processName\":\"" << processName << "\","
       << "\"memoryUsageMB\":" << memoryUsageMB << ","
       << "\"cpuUsagePercent\":" << cpuUsagePercent << ","
       << "\"threadCount\":" << threadCount
       << "}";
    return ss.str();
}

std::string SystemMetrics::toCsvHeader() const {
    return "Timestamp,ProcessName,MemoryMB,CPUPercent,ThreadCount";
}

std::string SystemMetrics::toCsvRow() const {
    std::stringstream ss;
    ss << getTimestamp() << ","
       << processName << ","
       << memoryUsageMB << ","
       << cpuUsagePercent << ","
       << threadCount;
    return ss.str();
}