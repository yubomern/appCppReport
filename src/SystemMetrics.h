#pragma once
#include <string>
#include <chrono>
#include <cstdint>

class SystemMetrics {
private:
    uint64_t memoryUsageMB;
    uint64_t cpuUsagePercent;
    uint64_t threadCount;
    std::chrono::system_clock::time_point timestamp;
    std::string processName;

public:
    SystemMetrics();
    explicit SystemMetrics(const std::string& procName);
    ~SystemMetrics() = default;

    void collect();
    
    // Getters
    uint64_t getMemoryUsage() const { return memoryUsageMB; }
    uint64_t getCpuUsage() const { return cpuUsagePercent; }
    uint64_t getThreadCount() const { return threadCount; }
    std::string getTimestamp() const;
    std::string getProcessName() const { return processName; }
    
    // Serialization
    std::string toJson() const;
    std::string toCsvHeader() const;
    std::string toCsvRow() const;
};