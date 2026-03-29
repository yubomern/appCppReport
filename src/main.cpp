#include "CoreDumpManager.h"
#include "PlatformUtils.h"
#include "CrashExporterFactory.h"
#include <iostream>
#include <memory>
#include <string>

void printUsage(const char* programName) {
    std::cout << "Usage: " << programName << " [options]\n"
              << "Options:\n"
              << "  --dump <path>     Path to core dump file\n"
              << "  --export <format> Export format (json/csv)\n"
              << "  --output <path>   Output file path (without extension)\n"
              << "  --help            Show this help\n"
              << "\nExample:\n"
              << "  " << programName << " --dump crash.dmp --export json --output crash_report\n";
}

int main(int argc, char* argv[]) {
    std::cout << "Crash Dump Analyzer v1.0\n";
    std::cout << "Running on: " << PlatformUtils::getPlatformName() << "\n\n";
    
    // Parse command line arguments
    std::string dumpPath = "default_crash.dmp";
    std::string exportFormat = "json";
    std::string outputPath = "crash_report";
    bool showHelp = false;
    
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--dump" && i + 1 < argc) {
            dumpPath = argv[++i];
        } else if (arg == "--export" && i + 1 < argc) {
            exportFormat = argv[++i];
        } else if (arg == "--output" && i + 1 < argc) {
            outputPath = argv[++i];
        } else if (arg == "--help") {
            showHelp = true;
        }
    }
    
    if (showHelp) {
        printUsage(argv[0]);
        return 0;
    }
    
    // Create the manager (uses composition)
    auto manager = std::make_unique<CoreDumpManager>();
    
    // Initialize crash data
    std::string appName = PlatformUtils::getProcessName();
    manager->initializeCrashData(appName);
    
    // Capture/simulate crash
    std::cout << "Processing crash dump: " << dumpPath << "\n";
    manager->captureCrash(dumpPath);
    
    // Print summary
    manager->printCrashSummary();
    
    // Export in requested format
    std::cout << "Exporting crash data to " << exportFormat << " format...\n";
    if (manager->exportCrashData(outputPath, exportFormat)) {
        std::cout << "Export completed successfully!\n";
    } else {
        std::cout << "Export failed!\n";
        return 1;
    }
    
    // Demonstrate polymorphism with different exporters
    std::cout << "\nDemonstrating polymorphism:\n";
    std::cout << "----------------------------------------\n";
    
    auto jsonExporter = CrashExporterFactory::create(ExportFormat::JSON);
    std::cout << "Created exporter: " << jsonExporter->getFormatName() 
              << " (extension: " << jsonExporter->getFileExtension() << ")\n";
    
    auto csvExporter = CrashExporterFactory::create(ExportFormat::CSV);
    std::cout << "Created exporter: " << csvExporter->getFormatName() 
              << " (extension: " << csvExporter->getFileExtension() << ")\n";
    
    std::cout << "\nAll operations completed successfully!\n";
    
    return 0;
}