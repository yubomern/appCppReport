import streamlit as st
import sqlite3
import pandas as pd
import json
import plotly.express as px

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="CoreDump Dashboard", layout="wide")
st.title("💥 Advanced CoreDump Dashboard")

DB_PATH = "crashs.db"

# -------------------------
# INIT DB
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS crashes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT,
        process_id INTEGER,
        crash_time TEXT,
        reason TEXT,
        cpu REAL,
        memory REAL,
        threads INTEGER
    )
    """)
    
    conn.commit()
    conn.close()

init_db()

# -------------------------
# INSERT JSON
# -------------------------
def insert_json(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    INSERT INTO crashes (app_name, process_id, crash_time, reason, cpu, memory, threads)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["applicationName"],
        data["processId"],
        data["crashTime"],
        data["crashAnalysis"]["crashReason"],
        data["systemMetrics"]["cpuUsagePercent"],
        data["systemMetrics"]["memoryUsageMB"],
        data["systemMetrics"]["threadCount"]
    ))
    
    conn.commit()
    conn.close()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("⚙️ Options")

uploaded_file = st.sidebar.file_uploader("Upload JSON", type="json")

if uploaded_file:
    data = json.load(uploaded_file)
    insert_json(data)
    st.sidebar.success("Crash ajouté ✅")

# -------------------------
# LOAD DATA
# -------------------------
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM crashes", conn)
conn.close()

# -------------------------
# FILTERS
# -------------------------
st.sidebar.header("🔍 Filtres")

if not df.empty:
    reasons = st.sidebar.multiselect(
        "Crash Reason",
        df["reason"].unique(),
        default=df["reason"].unique()
    )
    
    df = df[df["reason"].isin(reasons)]

# -------------------------
# KPIs
# -------------------------
st.header("📊 KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total Crashes", len(df))
col2.metric("Avg CPU", round(df["cpu"].mean(), 2) if not df.empty else 0)
col3.metric("Avg Memory", round(df["memory"].mean(), 2) if not df.empty else 0)

# -------------------------
# TABLE
# -------------------------
st.header("📋 Crash Data")

st.dataframe(df, use_container_width=True)

# -------------------------
# CHARTS
# -------------------------
st.header("📈 Visualisation")

if not df.empty:

    # Pie chart (reasons)
    fig1 = px.pie(df, names="reason", title="Crash Reasons Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    # CPU chart
    fig2 = px.line(df, y="cpu", title="CPU Usage Over Crashes")
    st.plotly_chart(fig2, use_container_width=True)

    # Memory chart
    fig3 = px.bar(df, x="id", y="memory", title="Memory Usage")
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# DETAILS VIEW
# -------------------------
st.header("🔍 Crash Details")

if not df.empty:
    selected_id = st.selectbox("Select Crash ID", df["id"])
    selected = df[df["id"] == selected_id].iloc[0]

    st.write("### Details")
    st.json({
        "Application": selected["app_name"],
        "Process ID": selected["process_id"],
        "Crash Time": selected["crash_time"],
        "Reason": selected["reason"]
    })

# -------------------------
# EXPORT
# -------------------------
st.header("📤 Export")

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "crashes.csv",
    "text/csv"
)