#pragma once
#include <string>
#include <memory>

class CoreDumpData;  // Forward declaration

// Interface for polymorphism
class ICrashExporter {
public:
    virtual ~ICrashExporter() = default;
    
    virtual bool exportData(const CoreDumpData& data, const std::string& outputPath) = 0;
    virtual std::string getFormatName() const = 0;
    virtual std::string getFileExtension() const = 0;
};