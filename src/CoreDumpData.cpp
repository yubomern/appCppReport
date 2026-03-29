#include "CoreDumpData.h"
#include <sstream>
#include <iomanip>

CoreDumpData::CoreDumpData() 
    : systemMetrics(std::make_unique<SystemMetrics>()),
      crashAnalysis(std::make_unique<CrashAnalysis>()),
      dumpFilePath(""),
      processId(0),
      applicationName("") {
    crashTime = std::chrono::system_clock::now();
}

void CoreDumpData::initialize(const std::string& appName, uint64_t pid) {
    applicationName = appName;
    processId = pid;
    crashTime = std::chrono::system_clock::now();
    systemMetrics = std::make_unique<SystemMetrics>(appName);
}

void CoreDumpData::collectCrashData(const std::string& dumpPath) {
    dumpFilePath = dumpPath;
    crashTime = std::chrono::system_clock::now();
    
    // Collect system metrics at crash time
    if (systemMetrics) {
        systemMetrics->collect();
    }
    
    // Analyze the crash
    if (crashAnalysis) {
        crashAnalysis->analyze(dumpPath);
    }
}

std::string CoreDumpData::getCrashTime() const {
    auto time = std::chrono::system_clock::to_time_t(crashTime);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
    return ss.str();
}

std::string CoreDumpData::toJson() const {
    std::stringstream ss;
    ss << "{"
       << "\"applicationName\":\"" << applicationName << "\","
       << "\"processId\":" << processId << ","
       << "\"crashTime\":\"" << getCrashTime() << "\","
       << "\"dumpFilePath\":\"" << dumpFilePath << "\","
       << "\"systemMetrics\":" << (systemMetrics ? systemMetrics->toJson() : "{}") << ","
       << "\"crashAnalysis\":" << (crashAnalysis ? crashAnalysis->toJson() : "{}")
       << "}";
    return ss.str();
}