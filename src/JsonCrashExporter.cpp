#include "JsonCrashExporter.h"
#include "CoreDumpData.h"
#include <iostream>
#include <fstream>
bool JsonCrashExporter::exportData(const CoreDumpData& data, const std::string& outputPath) {
    std::string jsonContent = data.toJson();
    return writeToFile(jsonContent, outputPath);
}

bool JsonCrashExporter::writeToFile(const std::string& content, const std::string& path) {
    std::ofstream file(path);
    if (!file.is_open()) {
        return false;
    }
    
    file << content;
    file.close();
    return true;
}