#pragma once
#include <memory>
#include <string>
#include "ICrashExporter.h"

enum class ExportFormat {
    JSON,
    CSV
};

class CrashExporterFactory {
public:
    // Factory pattern: creates exporters dynamically
    static std::unique_ptr<ICrashExporter> create(ExportFormat format);
    static std::unique_ptr<ICrashExporter> createFromString(const std::string& format);
    
    static ExportFormat stringToFormat(const std::string& format);
    static std::string formatToString(ExportFormat format);
};