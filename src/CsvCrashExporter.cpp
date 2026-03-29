#include "CsvCrashExporter.h"
#include "CoreDumpData.h"
#include <sstream>

bool CsvCrashExporter::exportData(const CoreDumpData& data, const std::string& outputPath) {
    std::stringstream ss;
    
    // Create CSV content
    ss << "Application,ProcessId,CrashTime,DumpPath\n";
    ss << data.getApplicationName() << ","
       << data.getProcessId() << ","
       << data.getCrashTime() << ","
       << data.getDumpFilePath() << "\n\n";
    
    // Add metrics if available
    if (data.getSystemMetrics()) {
        ss << "\n# System Metrics\n";
        ss << data.getSystemMetrics()->toCsvHeader() << "\n";
        ss << data.getSystemMetrics()->toCsvRow() << "\n";
    }
    
    // Add crash analysis if available
    if (data.getCrashAnalysis()) {
        ss << "\n# Crash Analysis\n";
        ss << data.getCrashAnalysis()->toCsvHeader() << "\n";
        ss << data.getCrashAnalysis()->toCsvRow() << "\n";
    }
    
    return writeToFile(ss.str(), outputPath);
}

bool CsvCrashExporter::writeToFile(const std::string& content, const std::string& path) {
    std::ofstream file(path);
    if (!file.is_open()) {
        return false;
    }
    
    file << content;
    file.close();
    return true;
}