#include "CoreDumpManager.h"
#include "PlatformUtils.h"
#include "CrashExporterFactory.h"
#include <iostream>
#include <iomanip>

CoreDumpManager::CoreDumpManager() 
    : crashData(std::make_unique<CoreDumpData>()) {
    // Register crash handler using PlatformUtils (Association)
    PlatformUtils::registerCrashHandler();
}

void CoreDumpManager::initializeCrashData(const std::string& appName) {
    uint64_t pid = PlatformUtils::getCurrentProcessId();
    crashData->initialize(appName, pid);
    
    PlatformUtils::logToSystem("Crash data initialized for: " + appName + " (PID: " + std::to_string(pid) + ")");
}

void CoreDumpManager::captureCrash(const std::string& dumpPath) {
    PlatformUtils::logToSystem("Capturing crash from: " + dumpPath);
    
    // Collect crash data
    crashData->collectCrashData(dumpPath);
    
    // Generate minidump using PlatformUtils
    PlatformUtils::generateMiniDump(dumpPath);
    
    PlatformUtils::logToSystem("Crash captured successfully");
}

bool CoreDumpManager::exportCrashData(const std::string& outputPath, const std::string& format) {
    // Dependency: temporary use of CrashExporterFactory (not stored as member)
    auto exporter = CrashExporterFactory::createFromString(format);
    
    if (!exporter) {
        PlatformUtils::logToSystem("Failed to create exporter for format: " + format, 2);
        return false;
    }
    
    std::string fullPath = outputPath + exporter->getFileExtension();
    bool result = exporter->exportData(*crashData, fullPath);
    
    if (result) {
        PlatformUtils::logToSystem("Exported crash data to: " + fullPath + " (" + exporter->getFormatName() + ")");
    } else {
        PlatformUtils::logToSystem("Failed to export crash data", 2);
    }
    
    return result;
}

void CoreDumpManager::printCrashSummary() const {
    std::cout << "\n" << std::string(60, '=') << "\n";
    std::cout << "CRASH DUMP SUMMARY\n";
    std::cout << std::string(60, '=') << "\n";
    std::cout << "Platform: " << PlatformUtils::getPlatformName() << "\n";
    std::cout << "Application: " << crashData->getApplicationName() << "\n";
    std::cout << "Process ID: " << crashData->getProcessId() << "\n";
    std::cout << "Crash Time: " << crashData->getCrashTime() << "\n";
    std::cout << "Dump Path: " << crashData->getDumpFilePath() << "\n";
    
    if (crashData->getSystemMetrics()) {
        std::cout << "\nSystem Metrics:\n";
        std::cout << "  Memory: " << crashData->getSystemMetrics()->getMemoryUsage() << " MB\n";
        std::cout << "  CPU: " << crashData->getSystemMetrics()->getCpuUsage() << "%\n";
        std::cout << "  Threads: " << crashData->getSystemMetrics()->getThreadCount() << "\n";
    }
    
    if (crashData->getCrashAnalysis()) {
        std::cout << "\nCrash Analysis:\n";
        std::cout << "  Reason: " << crashData->getCrashAnalysis()->getCrashReason() << "\n";
        std::cout << "  Address: " << crashData->getCrashAnalysis()->getCrashAddress() << "\n";
        std::cout << "  Exception: " << crashData->getCrashAnalysis()->getExceptionCode() << "\n";
    }
    
    std::cout << std::string(60, '=') << "\n\n";
}