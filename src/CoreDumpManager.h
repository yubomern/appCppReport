#pragma once
#include <memory>
#include <string>
#include "CoreDumpData.h"
#include "ICrashExporter.h"

// Forward declaration
class CrashExporterFactory;

class CoreDumpManager {
private:
    // Composition: CoreDumpManager OWNS CoreDumpData
    std::unique_ptr<CoreDumpData> crashData;
    
    // Association: uses PlatformUtils (not owned, static methods)
    
public:
    CoreDumpManager();
    ~CoreDumpManager() = default;
    
    void initializeCrashData(const std::string& appName);
    void captureCrash(const std::string& dumpPath);
    
    // Dependency: uses CrashExporterFactory only during export
    bool exportCrashData(const std::string& outputPath, const std::string& format);
    
    CoreDumpData* getCrashData() { return crashData.get(); }
    const CoreDumpData* getCrashData() const { return crashData.get(); }
    
    void printCrashSummary() const;
};