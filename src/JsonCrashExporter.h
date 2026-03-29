#pragma once
#include "ICrashExporter.h"
#include <fstream>

class JsonCrashExporter : public ICrashExporter {
public:
    JsonCrashExporter() = default;
    ~JsonCrashExporter() override = default;
    
    bool exportData(const CoreDumpData& data, const std::string& outputPath) override;
    std::string getFormatName() const override { return "JSON"; }
    std::string getFileExtension() const override { return ".json"; }
    
private:
    bool writeToFile(const std::string& content, const std::string& path);
};