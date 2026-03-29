Application        CoreDumpManager       PlatformUtils      CoreDumpData      CrashExporterFactory      ICrashExporter
     |                    |                     |                  |                    |                       |
     |---- Store() -----> |                     |                  |                    |                       |
     |                    |---- CaptureCallStack() -------------> |                    |                       |
     |                    |<----------- stackTrace ---------------|                    |                       |
     |                    |---- setMetadata() -------------------> |                    |                       |
     |                    |---- setStackTrace() -----------------> |                    |                       |
     |                    |---- Analyze() -----------------------> |                    |                       |
     |                    |---- setAnalysis() -------------------> |                    |                       |
     |                    |                     |                  |                    |                       |
     |---- Export() ----> |                     |                  |                    |                       |
     |                    |---- Create(format) ------------------------------->          |                       |
     |                    |<--- unique_ptr<ICrashExporter> -------------------|          |                       |
     |                    |--------------------------------------------------------------> Export(data,path)     |
     |                    |                     |                  |                    |                       |
     |                    |<---------------------- fichier écrit ------------------------|                       |



     Participants: Application, CoreDumpManager, PlatformUtils, CoreDumpData, CrashExporterFactory, ICrashExporter

Sequence:

Application -> CoreDumpManager: Store(file, line)
CoreDumpManager -> PlatformUtils: CaptureCallStack()
PlatformUtils -> CoreDumpManager: stackTrace
CoreDumpManager -> CoreDumpData: setMetadata(), setStackTrace()
CoreDumpManager -> CoreDumpData: Analyze()
Application -> CoreDumpManager: Export(format)
CoreDumpManager -> CrashExporterFactory: Create(format)
CrashExporterFactory -> CoreDumpManager: unique_ptr<ICrashExporter>
CoreDumpManager -> ICrashExporter: Export(data, path)
ICrashExporter -> FileSystem: write file

