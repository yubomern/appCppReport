mkdir build
cd build
cmake .. -G "MinGW Makefiles"
cmake --build . --config Release
.\bin\CrashDumpAnalyzer.exe --dump test.dmp --export json --output report