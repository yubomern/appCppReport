#pragma once
#include <memory>
#include <string>
#include <chrono>
#include <cstdint>

#include "SystemMetrics.h"
#include "CrashAnalysis.h"

class CoreDumpData {
private:
    std::unique_ptr<SystemMetrics> systemMetrics;
    std::unique_ptr<CrashAnalysis> crashAnalysis;
    std::string dumpFilePath;
    std::chrono::system_clock::time_point crashTime;
    uint64_t processId;
    std::string applicationName;

public:
    CoreDumpData();
    ~CoreDumpData() = default;
    
    // Composition: CoreDumpData OWNS SystemMetrics and CrashAnalysis
    void initialize(const std::string& appName, uint64_t pid);
    void collectCrashData(const std::string& dumpPath);
    
    // Getters (expose owned objects)
    SystemMetrics* getSystemMetrics() { return systemMetrics.get(); }
    const SystemMetrics* getSystemMetrics() const { return systemMetrics.get(); }
    
    CrashAnalysis* getCrashAnalysis() { return crashAnalysis.get(); }
    const CrashAnalysis* getCrashAnalysis() const { return crashAnalysis.get(); }
    
    std::string getDumpFilePath() const { return dumpFilePath; }
    std::string getCrashTime() const;
    uint64_t getProcessId() const { return processId; }
    std::string getApplicationName() const { return applicationName; }
    
    // Serialization
    std::string toJson() const;
};