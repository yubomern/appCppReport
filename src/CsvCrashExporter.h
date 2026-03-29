#pragma once
#include "ICrashExporter.h"
#include <fstream>

class CsvCrashExporter : public ICrashExporter {
public:
    CsvCrashExporter() = default;
    ~CsvCrashExporter() override = default;
    
    bool exportData(const CoreDumpData& data, const std::string& outputPath) override;
    std::string getFormatName() const override { return "CSV"; }
    std::string getFileExtension() const override { return ".csv"; }
    
private:
    bool writeToFile(const std::string& content, const std::string& path);
};