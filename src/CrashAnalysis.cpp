#include "CrashAnalysis.h"
#include <sstream>
#include <iomanip>

CrashAnalysis::CrashAnalysis() 
    : crashReason("Unknown"), 
      crashAddress("0x00000000"),
      moduleName("unknown"),
      exceptionCode("0x00000000"),
      isRecoverable(false) {
}

void CrashAnalysis::analyze(const std::string& dumpPath) {
    // Simulate crash analysis
    // In a real implementation, this would parse the core dump file
    
    crashReason = "Segmentation Fault (Access Violation)";
    crashAddress = "0x7fff5bf041c8";
    moduleName = dumpPath.substr(dumpPath.find_last_of("/\\") + 1);
    exceptionCode = "0xC0000005";  // Access violation on Windows
    
    // Simulate call stack
    StackFrame frame1{"CrashFunction()", "application.cpp", 42, 0x7fff5bf041c8};
    StackFrame frame2{"ProcessRequest()", "handler.cpp", 128, 0x7fff5bf04200};
    StackFrame frame3{"MainLoop()", "main.cpp", 256, 0x7fff5bf04350};
    
    callStack.push_back(frame1);
    callStack.push_back(frame2);
    callStack.push_back(frame3);
    
    isRecoverable = false;
}

void CrashAnalysis::addStackFrame(const StackFrame& frame) {
    callStack.push_back(frame);
}

std::string CrashAnalysis::toJson() const {
    std::stringstream ss;
    ss << "{"
       << "\"crashReason\":\"" << crashReason << "\","
       << "\"crashAddress\":\"" << crashAddress << "\","
       << "\"moduleName\":\"" << moduleName << "\","
       << "\"exceptionCode\":\"" << exceptionCode << "\","
       << "\"isRecoverable\":" << (isRecoverable ? "true" : "false") << ","
       << "\"callStack\":[";
    
    for (size_t i = 0; i < callStack.size(); ++i) {
        if (i > 0) ss << ",";
        ss << "{"
           << "\"function\":\"" << callStack[i].function << "\","
           << "\"file\":\"" << callStack[i].file << "\","
           << "\"line\":" << callStack[i].lineNumber << ","
           << "\"address\":\"" << std::hex << callStack[i].address << std::dec << "\""
           << "}";
    }
    
    ss << "]}";
    return ss.str();
}

std::string CrashAnalysis::toCsvHeader() const {
    return "CrashReason,CrashAddress,ModuleName,ExceptionCode,IsRecoverable,CallStackFrames";
}

std::string CrashAnalysis::toCsvRow() const {
    std::stringstream ss;
    ss << "\"" << crashReason << "\","
       << "\"" << crashAddress << "\","
       << "\"" << moduleName << "\","
       << "\"" << exceptionCode << "\","
       << (isRecoverable ? "Yes" : "No") << ","
       << callStack.size();
    return ss.str();
}