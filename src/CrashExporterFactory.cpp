// #include "CrashExporterFactory.h"
// #include "JsonCrashExporter.h"
// #include "CsvCrashExporter.h"
// #include <algorithm>
// #include <cctype>

// std::unique_ptr<ICrashExporter> CrashExporterFactory::create(ExportFormat format) {
//     switch (format) {
//         case ExportFormat::JSON:
//             return std::make_unique<JsonCrashExporter>();
//         case ExportFormat::CSV:
//             return std::make_unique<CsvCrashExporter>();
//         default:
//             return nullptr;
//     }
// }

// std::unique_ptr<ICrashExporter> CrashExporterFactory::createFromString(const std::string& format) {
//     std::string lowerFormat = format;
//     std::transform(lowerFormat.begin(), lowerFormat.end(), lowerFormat.begin(), ::tolower);
    
//     if (lowerFormat == "json") {
//         return create(ExportFormat::JSON);
//     } else if (lowerFormat == "csv") {
//         return create(ExportFormat::CSV);
//     }
    
//     return nullptr;
// }

// ExportFormat CrashExporterFactory::stringToFormat(const std::string& format) {
//     std::string lowerFormat = format;
//     std::transform(lowerFormat.begin(), lowerFormat.end(), lowerFormat.begin(), ::tolower);
    
//     if (lowerFormat == "json") return ExportFormat::JSON;
//     return ExportFormat::CSV;
// }

// std::string CrashExporterFactory::formatToString(ExportFormat format) {
//     switch (format) {
//         case ExportFormat::JSON: return "JSON";
//         case ExportFormat::CSV: return "CSV";
//         default: return "Unknown";
//     }
// }


#include "CrashExporterFactory.h"
#include "JsonCrashExporter.h"
#include "CsvCrashExporter.h"
#include <algorithm>
#include <cctype>

std::unique_ptr<ICrashExporter> CrashExporterFactory::create(ExportFormat format) {
    switch (format) {
        case ExportFormat::JSON:
            return std::make_unique<JsonCrashExporter>();
        case ExportFormat::CSV:
            return std::make_unique<CsvCrashExporter>();
        default:
            return nullptr;
    }
}

std::unique_ptr<ICrashExporter> CrashExporterFactory::createFromString(const std::string& format) {
    std::string lowerFormat = format;
    std::transform(lowerFormat.begin(), lowerFormat.end(), lowerFormat.begin(), ::tolower);
    
    if (lowerFormat == "json") {
        return create(ExportFormat::JSON);
    } else if (lowerFormat == "csv") {
        return create(ExportFormat::CSV);
    }
    
    return nullptr;
}

ExportFormat CrashExporterFactory::stringToFormat(const std::string& format) {
    std::string lowerFormat = format;
    std::transform(lowerFormat.begin(), lowerFormat.end(), lowerFormat.begin(), ::tolower);
    
    if (lowerFormat == "json") return ExportFormat::JSON;
    return ExportFormat::CSV;
}

std::string CrashExporterFactory::formatToString(ExportFormat format) {
    switch (format) {
        case ExportFormat::JSON: return "JSON";
        case ExportFormat::CSV: return "CSV";
        default: return "Unknown";
    }
}