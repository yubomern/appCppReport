#pragma once
#include <string>
#include <vector>

struct StackFrame {
    std::string function;
    std::string file;
    int lineNumber;
    uintptr_t address;
};

class CrashAnalysis {
private:
    std::string crashReason;
    std::string crashAddress;
    std::vector<StackFrame> callStack;
    std::string moduleName;
    std::string exceptionCode;
    bool isRecoverable;

public:
    CrashAnalysis();
    ~CrashAnalysis() = default;
    
    void analyze(const std::string& dumpPath);
    void addStackFrame(const StackFrame& frame);
    
    // Getters
    std::string getCrashReason() const { return crashReason; }
    std::string getCrashAddress() const { return crashAddress; }
    std::vector<StackFrame> getCallStack() const { return callStack; }
    std::string getModuleName() const { return moduleName; }
    std::string getExceptionCode() const { return exceptionCode; }
    bool isRecoverableCrash() const { return isRecoverable; }
    
    // Serialization
    std::string toJson() const;
    std::string toCsvHeader() const;
    std::string toCsvRow() const;
};