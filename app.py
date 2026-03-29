import streamlit as st
import json
import pandas as pd

# ------------------------
# CONFIG
# ------------------------
st.set_page_config(page_title="CoreDump Dashboard", layout="wide")

st.title("💥 CoreDump Crash Analyzer Dashboard")

# ------------------------
# LOAD JSON
# ------------------------
with open("report.json", "r") as f:
    data = json.load(f)

# ------------------------
# BASIC INFO
# ------------------------
st.header("📌 Informations Générales")

col1, col2, col3 = st.columns(3)

col1.metric("Application", data["applicationName"])
col2.metric("Process ID", data["processId"])
col3.metric("Crash Time", data["crashTime"])

st.write("📂 Dump file:", data["dumpFilePath"])

# ------------------------
# SYSTEM METRICS
# ------------------------
st.header("📊 System Metrics")

metrics = data["systemMetrics"]

col1, col2, col3 = st.columns(3)

col1.metric("Memory (MB)", metrics["memoryUsageMB"])
col2.metric("CPU (%)", metrics["cpuUsagePercent"])
col3.metric("Threads", metrics["threadCount"])

# ------------------------
# CRASH ANALYSIS
# ------------------------
st.header("🚨 Crash Analysis")

analysis = data["crashAnalysis"]

st.error(f"Reason: {analysis['crashReason']}")
st.write("Address:", analysis["crashAddress"])
st.write("Exception Code:", analysis["exceptionCode"])
st.write("Module:", analysis["moduleName"])

if analysis["isRecoverable"]:
    st.success("Recoverable Crash ✅")
else:
    st.warning("Non-recoverable Crash ❌")

# ------------------------
# CALL STACK
# ------------------------
st.header("🧵 Call Stack")

callstack = analysis["callStack"]
df = pd.DataFrame(callstack)

st.dataframe(df, use_container_width=True)

# ------------------------
# CHART
# ------------------------
st.header("📈 Metrics Visualization")

chart_data = pd.DataFrame({
    "Metric": ["Memory", "CPU", "Threads"],
    "Value": [
        metrics["memoryUsageMB"],
        metrics["cpuUsagePercent"],
        metrics["threadCount"]
    ]
})

st.bar_chart(chart_data.set_index("Metric"))

# ------------------------
# EXPORT BUTTON
# ------------------------
st.header("📤 Export")

st.download_button(
    label="Download JSON Report",
    data=json.dumps(data, indent=4),
    file_name="report.json",
    mime="application/json"
)