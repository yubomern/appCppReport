import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import glob
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Crash Dump Analyzer - Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    /* Warning box */
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Success box */
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Info box */
    .info-box {
        background: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data(ttl=300)
def load_csv_files(directory):
    """Load all CSV files from a directory"""
    dataframes = []
    
    if not os.path.exists(directory):
        return dataframes
    
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            st.warning(f"Could not load {file}: {e}")
    
    return dataframes

@st.cache_data(ttl=300)
def load_json_files(directory):
    """Load all JSON files from a directory"""
    json_data = []
    
    if not os.path.exists(directory):
        return json_data
    
    json_files = glob.glob(os.path.join(directory, "*.json"))
    
    for file in json_files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                json_data.append(data)
        except Exception as e:
            st.warning(f"Could not load {file}: {e}")
    
    return json_data

@st.cache_data(ttl=300)
def parse_crash_report(file_path):
    """Parse a detailed crash report CSV file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        crash_data = {}
        
        # Extract application info
        lines = content.split('\n')
        for line in lines:
            if line.startswith('Application,'):
                parts = line.split(',')
                if len(parts) >= 4:
                    crash_data['Application'] = parts[0]
                    crash_data['Process ID'] = parts[1]
                    crash_data['Crash Time'] = parts[2]
                    crash_data['Dump Path'] = parts[3]
            
            # Extract metrics
            elif 'MemoryMB' in line or 'Memory (MB)' in line:
                continue
            elif line and not line.startswith('#') and ',' in line:
                parts = line.split(',')
                if len(parts) >= 5 and any(c.isdigit() for c in parts[2]) if len(parts) > 2 else False:
                    try:
                        crash_data['Memory (MB)'] = float(parts[2]) if parts[2] else 0
                        crash_data['CPU %'] = float(parts[3]) if parts[3] else 0
                        crash_data['Threads'] = int(parts[4]) if parts[4] else 0
                    except:
                        pass
            
            # Extract crash reason
            elif 'CrashReason' in line or 'Crash Reason' in line:
                continue
            elif 'Segmentation' in line or 'Access Violation' in line or 'Null' in line:
                parts = line.split(',')
                if len(parts) >= 1:
                    crash_data['Crash Reason'] = parts[0].strip('"')
                    if len(parts) >= 2:
                        crash_data['Exception Code'] = parts[3].strip('"') if len(parts) > 3 else parts[1].strip('"')
        
        return crash_data if crash_data else None
    except Exception as e:
        return None

@st.cache_data(ttl=300)
def create_dataframe_from_crashes(crash_list):
    """Create a pandas DataFrame from crash data list"""
    if not crash_list:
        return pd.DataFrame()
    
    df = pd.DataFrame(crash_list)
    
    # Ensure required columns exist
    required_cols = ['Application', 'Crash Time', 'Memory (MB)', 'CPU %', 'Threads', 'Crash Reason']
    for col in required_cols:
        if col not in df.columns:
            df[col] = 'Unknown' if col in ['Application', 'Crash Reason'] else 0
    
    # Convert Crash Time to datetime
    if 'Crash Time' in df.columns:
        df['Crash Time'] = pd.to_datetime(df['Crash Time'], errors='coerce')
    
    return df

# ============================================================================
# DEMO DATA GENERATION
# ============================================================================

def generate_demo_data():
    """Generate demo data for visualization"""
    np.random.seed(42)
    
    applications = ['WebServer', 'DatabaseEngine', 'GameClient', 
                   'VideoEditor', 'CompressionTool', 'Antivirus',
                   'Browser', 'MediaPlayer', 'OfficeSuite', 'IDE']
    
    crash_reasons = [
        'Segmentation Fault', 'Access Violation', 'Stack Overflow',
        'Heap Corruption', 'Null Pointer Dereference', 'Double Free',
        'Invalid Parameter', 'Out of Memory', 'Assertion Failed',
        'Deadlock Detected'
    ]
    
    exception_codes = [
        '0xC0000005', '0xC00000FD', '0xC0000374', 
        '0x80000003', '0xC0000094', '0xE06D7363'
    ]
    
    data = []
    
    for i in range(150):
        crash_time = datetime.now() - timedelta(
            days=np.random.randint(0, 90),
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60)
        )
        
        app = np.random.choice(applications)
        memory_mb = np.random.normal(250, 120)
        memory_mb = max(10, min(1200, memory_mb))
        
        cpu_percent = np.random.normal(45, 35)
        cpu_percent = max(0, min(100, cpu_percent))
        
        threads = int(np.random.normal(25, 15))
        threads = max(1, threads)
        
        crash_reason = np.random.choice(crash_reasons)
        exception_code = np.random.choice(exception_codes)
        stack_frames = np.random.randint(3, 35)
        
        data.append({
            'Application': app,
            'Process ID': np.random.randint(1000, 99999),
            'Crash Time': crash_time,
            'Memory (MB)': round(memory_mb, 2),
            'CPU %': round(cpu_percent, 2),
            'Threads': threads,
            'Crash Reason': crash_reason,
            'Exception Code': exception_code,
            'Stack Frames': stack_frames,
            'Severity': np.random.choice(['Critical', 'High', 'Medium', 'Low'], p=[0.4, 0.3, 0.2, 0.1])
        })
    
    return pd.DataFrame(data)

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_memory_usage(df):
    """Create memory usage bar chart"""
    if df.empty:
        st.warning("No data available for memory usage chart")
        return
    
    # Group by application
    app_memory = df.groupby('Application')['Memory (MB)'].agg(['mean', 'max', 'min']).reset_index()
    app_memory.columns = ['Application', 'Average Memory (MB)', 'Max Memory (MB)', 'Min Memory (MB)']
    app_memory = app_memory.sort_values('Average Memory (MB)', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=app_memory['Average Memory (MB)'],
        y=app_memory['Application'],
        orientation='h',
        marker_color='lightcoral',
        name='Average',
        text=app_memory['Average Memory (MB)'].round(1),
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        x=app_memory['Max Memory (MB)'],
        y=app_memory['Application'],
        orientation='h',
        marker_color='darkred',
        name='Maximum',
        text=app_memory['Max Memory (MB)'].round(1),
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Memory Usage by Application",
        xaxis_title="Memory (MB)",
        yaxis_title="Application",
        height=500,
        barmode='group',
        hovermode='y unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_cpu_usage(df):
    """Create CPU usage visualization"""
    if df.empty:
        st.warning("No data available for CPU usage chart")
        return
    
    cpu_by_app = df.groupby('Application')['CPU %'].mean().sort_values(ascending=True)
    
    fig = px.bar(
        x=cpu_by_app.values,
        y=cpu_by_app.index,
        orientation='h',
        title="Average CPU Usage by Application",
        labels={'x': 'CPU Usage (%)', 'y': 'Application'},
        color=cpu_by_app.values,
        color_continuous_scale='Viridis',
        text=cpu_by_app.values.round(1)
    )
    
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=500, coloraxis_showscale=False)
    
    st.plotly_chart(fig, use_container_width=True)

def plot_crash_timeline(df):
    """Create crash timeline scatter plot"""
    if df.empty or 'Crash Time' not in df.columns:
        st.warning("No timeline data available")
        return
    
    # Filter out null dates
    df_valid = df[df['Crash Time'].notna()].copy()
    if df_valid.empty:
        st.warning("No valid dates in crash data")
        return
    
    df_valid = df_valid.sort_values('Crash Time')
    df_valid['Crash Count'] = range(1, len(df_valid) + 1)
    
    fig = px.scatter(
        df_valid,
        x='Crash Time',
        y='Crash Count',
        color='Severity' if 'Severity' in df_valid.columns else 'Crash Reason',
        size='Memory (MB)' if 'Memory (MB)' in df_valid.columns else None,
        hover_data=['Application', 'CPU %', 'Threads'],
        title="Crash Timeline",
        labels={'Crash Time': 'Date', 'Crash Count': 'Crash Number'}
    )
    
    fig.update_layout(height=500, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_crash_reasons(df):
    """Create crash reasons pie chart"""
    if df.empty:
        st.warning("No crash reason data available")
        return
    
    reason_counts = df['Crash Reason'].value_counts()
    
    # Group small categories as "Other"
    threshold = 5
    if len(reason_counts) > 10:
        small_categories = reason_counts[reason_counts < threshold]
        other_count = small_categories.sum()
        reason_counts = reason_counts[reason_counts >= threshold]
        if other_count > 0:
            reason_counts['Other'] = other_count
    
    fig = px.pie(
        values=reason_counts.values,
        names=reason_counts.index,
        title="Distribution of Crash Reasons",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    
    st.plotly_chart(fig, use_container_width=True)

def plot_resource_heatmap(df):
    """Create correlation heatmap"""
    if df.empty:
        st.warning("No data available for correlation heatmap")
        return
    
    numeric_cols = ['Memory (MB)', 'CPU %', 'Threads', 'Stack Frames']
    available_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(available_cols) < 2:
        st.warning("Need at least 2 numeric columns for correlation")
        return
    
    correlation = df[available_cols].corr()
    
    fig = px.imshow(
        correlation,
        text_auto=True,
        title="Resource Usage Correlation Matrix",
        color_continuous_scale='RdBu',
        aspect='auto',
        zmin=-1, zmax=1
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def plot_thread_distribution(df):
    """Create thread distribution histogram"""
    if df.empty or 'Threads' not in df.columns:
        st.warning("No thread data available")
        return
    
    fig = px.histogram(
        df,
        x='Threads',
        title="Thread Count Distribution",
        nbins=30,
        color_discrete_sequence=['#667eea'],
        marginal='box'
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def plot_severity_distribution(df):
    """Create severity distribution chart"""
    if df.empty or 'Severity' not in df.columns:
        return
    
    severity_order = ['Critical', 'High', 'Medium', 'Low']
    severity_counts = df['Severity'].value_counts()
    
    # Reorder
    severity_counts = severity_counts.reindex([s for s in severity_order if s in severity_counts])
    
    fig = px.bar(
        x=severity_counts.index,
        y=severity_counts.values,
        title="Crash Severity Distribution",
        labels={'x': 'Severity', 'y': 'Number of Crashes'},
        color=severity_counts.values,
        color_continuous_scale='Reds',
        text=severity_counts.values
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_top_applications(df):
    """Create top applications by crash count"""
    if df.empty:
        return
    
    app_crashes = df['Application'].value_counts().head(10)
    
    fig = px.bar(
        x=app_crashes.values,
        y=app_crashes.index,
        orientation='h',
        title="Top 10 Applications by Crash Count",
        labels={'x': 'Number of Crashes', 'y': 'Application'},
        color=app_crashes.values,
        color_continuous_scale='Blues',
        text=app_crashes.values
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(height=500, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_memory_trend(df):
    """Create memory usage trend over time"""
    if df.empty or 'Crash Time' not in df.columns:
        return
    
    df_valid = df[df['Crash Time'].notna()].copy()
    if df_valid.empty:
        return
    
    df_valid = df_valid.sort_values('Crash Time')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_valid['Crash Time'],
        y=df_valid['Memory (MB)'],
        mode='lines+markers',
        name='Memory Usage',
        line=dict(color='#667eea', width=2),
        marker=dict(size=8, color='#764ba2')
    ))
    
    fig.update_layout(
        title="Memory Usage Trend Over Time",
        xaxis_title="Date",
        yaxis_title="Memory (MB)",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Crash Dump Analyzer Dashboard</h1>
        <p>Real-time visualization and analysis of system crashes and performance metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/crash-test-dummy.png", width=80)
        st.markdown("## 📁 Data Source")
        
        # Data source selection
        data_source = st.radio(
            "Select Data Source",
            ["📂 Load Files", "🎲 Use Demo Data", "📝 Manual Entry"],
            help="Choose how to load crash data"
        )
        
        st.markdown("---")
        
        if data_source == "📂 Load Files":
            data_dir = st.text_input("Data Directory Path", value="./data")
            st.info(f"Looking for CSV/JSON files in: {data_dir}")
            
            if st.button("🔄 Refresh Data"):
                st.cache_data.clear()
                st.rerun()
        
        elif data_source == "📝 Manual Entry":
            st.markdown("### Enter Crash Data Manually")
            app_name = st.text_input("Application Name")
            memory = st.number_input("Memory Usage (MB)", min_value=0, max_value=10000, value=256)
            cpu = st.slider("CPU Usage (%)", 0, 100, 50)
            threads = st.number_input("Thread Count", min_value=1, max_value=500, value=25)
            crash_reason = st.selectbox("Crash Reason", [
                "Segmentation Fault", "Access Violation", "Stack Overflow",
                "Null Pointer", "Out of Memory", "Other"
            ])
            
            if st.button("➕ Add Crash Record"):
                st.session_state.manual_data = st.session_state.get('manual_data', [])
                st.session_state.manual_data.append({
                    'Application': app_name or "Unknown",
                    'Memory (MB)': memory,
                    'CPU %': cpu,
                    'Threads': threads,
                    'Crash Reason': crash_reason,
                    'Crash Time': datetime.now(),
                    'Process ID': np.random.randint(1000, 99999),
                    'Exception Code': "0x00000000",
                    'Stack Frames': np.random.randint(1, 20),
                    'Severity': "Medium"
                })
                st.success("Crash record added!")
        
        st.markdown("---")
        st.markdown("### 🎨 Visualization Settings")
        
        chart_height = st.slider("Chart Height", 300, 800, 500)
        show_animations = st.checkbox("Show Animations", value=True)
        
        st.markdown("---")
        st.markdown("### 📊 Export Options")
        
        if st.button("📥 Export Current View as CSV"):
            if 'df' in st.session_state and not st.session_state.df.empty:
                csv = st.session_state.df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "crash_data_export.csv",
                    "text/csv"
                )
    
    # Load data based on selection
    df = pd.DataFrame()
    
    if data_source == "📂 Load Files":
        data_dir = st.session_state.get('data_dir', './data')
        
        with st.spinner("Loading crash data..."):
            # Load CSV files
            csv_data = load_csv_files(data_dir)
            json_data = load_json_files(data_dir)
            
            crash_list = []
            
            # Process CSV files
            for csv_df in csv_data:
                crash_list.extend(csv_df.to_dict('records'))
            
            # Process detailed crash reports
            if os.path.exists(data_dir):
                for file in glob.glob(os.path.join(data_dir, "*.csv")):
                    parsed = parse_crash_report(file)
                    if parsed:
                        crash_list.append(parsed)
            
            # Process JSON files
            for json_obj in json_data:
                if isinstance(json_obj, dict):
                    crash_list.append(json_obj)
                elif isinstance(json_obj, list):
                    crash_list.extend(json_obj)
            
            if crash_list:
                df = create_dataframe_from_crashes(crash_list)
                st.success(f"✅ Loaded {len(df)} crash records from {data_dir}")
            else:
                st.warning("No crash data found. Please check the directory or use demo data.")
                if st.button("🎲 Load Demo Data Instead"):
                    df = generate_demo_data()
                    st.success(f"✅ Loaded {len(df)} demo crash records")
    
    elif data_source == "🎲 Use Demo Data":
        if st.button("🔄 Generate New Demo Data"):
            df = generate_demo_data()
            st.session_state.df = df
        else:
            if 'df' not in st.session_state or st.session_state.df.empty:
                df = generate_demo_data()
            else:
                df = st.session_state.df
        
        if not df.empty:
            st.success(f"✅ Using {len(df)} demo crash records")
    
    elif data_source == "📝 Manual Entry":
        if 'manual_data' in st.session_state and st.session_state.manual_data:
            df = pd.DataFrame(st.session_state.manual_data)
            st.success(f"✅ {len(df)} manual crash records")
        else:
            st.info("Add crash records using the form in the sidebar")
    
    # Store dataframe in session state
    st.session_state.df = df
    
    # Main content - only show if we have data
    if not df.empty:
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Dashboard", 
            "🔍 Detailed Analysis", 
            "📊 Statistics", 
            "📋 Raw Data",
            "ℹ️ About"
        ])
        
        with tab1:
            # Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Total Crashes</div>
                </div>
                """.format(len(df)), unsafe_allow_html=True)
            
            with col2:
                unique_apps = df['Application'].nunique()
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{}</div>
                    <div class="metric-label">Applications</div>
                </div>
                """.format(unique_apps), unsafe_allow_html=True)
            
            with col3:
                avg_memory = df['Memory (MB)'].mean() if 'Memory (MB)' in df.columns else 0
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{:.1f} MB</div>
                    <div class="metric-label">Avg Memory Usage</div>
                </div>
                """.format(avg_memory), unsafe_allow_html=True)
            
            with col4:
                avg_cpu = df['CPU %'].mean() if 'CPU %' in df.columns else 0
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-value">{:.1f}%</div>
                    <div class="metric-label">Avg CPU Usage</div>
                </div>
                """.format(avg_cpu), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Main visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Memory Usage Analysis")
                plot_memory_usage(df)
            
            with col2:
                st.subheader("⚡ CPU Usage Analysis")
                plot_cpu_usage(df)
            
            # Full width visualizations
            st.subheader("📅 Crash Timeline")
            plot_crash_timeline(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🥧 Crash Reasons Distribution")
                plot_crash_reasons(df)
            
            with col2:
                st.subheader("🔥 Resource Correlation")
                plot_resource_heatmap(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🧵 Thread Distribution")
                plot_thread_distribution(df)
            
            with col2:
                st.subheader("📈 Top Applications by Crashes")
                plot_top_applications(df)
            
            # Additional metrics if available
            if 'Severity' in df.columns:
                st.subheader("⚠️ Crash Severity Distribution")
                plot_severity_distribution(df)
            
            st.subheader("📉 Memory Usage Trend")
            plot_memory_trend(df)
        
        with tab2:
            st.markdown("## 🔍 Detailed Analysis")
            
            # Filters
            st.markdown("### Filter Data")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'Application' in df.columns:
                    selected_apps = st.multiselect(
                        "Filter by Application",
                        options=df['Application'].unique(),
                        default=df['Application'].unique()[:3] if len(df['Application'].unique()) > 3 else df['Application'].unique()
                    )
            
            with col2:
                if 'Crash Reason' in df.columns:
                    selected_reasons = st.multiselect(
                        "Filter by Crash Reason",
                        options=df['Crash Reason'].unique(),
                        default=[]
                    )
            
            with col3:
                if 'Memory (MB)' in df.columns:
                    memory_range = st.slider(
                        "Memory Range (MB)",
                        min_value=int(df['Memory (MB)'].min()),
                        max_value=int(df['Memory (MB)'].max()),
                        value=(int(df['Memory (MB)'].min()), int(df['Memory (MB)'].max()))
                    )
            
            # Apply filters
            filtered_df = df.copy()
            if selected_apps:
                filtered_df = filtered_df[filtered_df['Application'].isin(selected_apps)]
            if selected_reasons:
                filtered_df = filtered_df[filtered_df['Crash Reason'].isin(selected_reasons)]
            if 'Memory (MB)' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['Memory (MB)'] >= memory_range[0]) & 
                    (filtered_df['Memory (MB)'] <= memory_range[1])
                ]
            
            st.markdown(f"**Showing {len(filtered_df)} records**")
            
            # Summary statistics for filtered data
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Filtered Crashes", len(filtered_df))
            with col2:
                st.metric("Avg Memory", f"{filtered_df['Memory (MB)'].mean():.1f} MB" if not filtered_df.empty else "N/A")
            with col3:
                st.metric("Avg CPU", f"{filtered_df['CPU %'].mean():.1f}%" if not filtered_df.empty else "N/A")
            
            # Detailed breakdown
            st.markdown("### Crash Breakdown by Application")
            if not filtered_df.empty:
                breakdown = filtered_df.groupby(['Application', 'Crash Reason']).size().reset_index(name='Count')
                fig = px.bar(breakdown, x='Application', y='Count', color='Crash Reason',
                            title="Crashes by Application and Reason",
                            barmode='stack')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("## 📊 Statistical Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Descriptive Statistics")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if not numeric_cols.empty:
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)
            
            with col2:
                st.markdown("### Crash Frequency by Hour")
                if 'Crash Time' in df.columns and not df['Crash Time'].isna().all():
                    df['Hour'] = pd.to_datetime(df['Crash Time']).dt.hour
                    hour_counts = df['Hour'].value_counts().sort_index()
                    fig = px.bar(x=hour_counts.index, y=hour_counts.values,
                                title="Crashes by Hour of Day",
                                labels={'x': 'Hour', 'y': 'Number of Crashes'})
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Resource Usage Percentiles")
            if not numeric_cols.empty:
                percentiles = df[numeric_cols].quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
                st.dataframe(percentiles, use_container_width=True)
            
            st.markdown("### Top Crash Patterns")
            if 'Crash Reason' in df.columns and 'Application' in df.columns:
                patterns = df.groupby(['Application', 'Crash Reason']).size().sort_values(ascending=False).head(10)
                st.dataframe(pd.DataFrame(patterns, columns=['Count']), use_container_width=True)
        
        with tab4:
            st.markdown("## 📋 Raw Data")
            
            # Search functionality
            search_term = st.text_input("🔍 Search in data", placeholder="Enter search term...")
            
            if search_term:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False).any(), axis=1)
                display_df = df[mask]
                st.info(f"Found {len(display_df)} matching records")
            else:
                display_df = df
            
            # Show number of rows
            rows_to_show = st.slider("Rows to display", 10, 100, 50)
            st.dataframe(display_df.head(rows_to_show), use_container_width=True)
            
            # Export buttons
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False)
                st.download_button("📥 Download All Data (CSV)", csv, "all_crash_data.csv", "text/csv")
            with col2:
                json_str = df.to_json(orient='records', indent=2)
                st.download_button("📥 Download All Data (JSON)", json_str, "all_crash_data.json", "application/json")
        
        with tab5:
            st.markdown("""
            <div class="info-box">
                <h3>ℹ️ About Crash Dump Analyzer</h3>
                <p>A comprehensive tool for analyzing and visualizing system crashes and performance metrics.</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🚀 Features
                
                - **Real-time Monitoring**: Track system crashes as they happen
                - **Interactive Visualizations**: Dynamic charts and graphs
                - **Multi-format Support**: CSV, JSON, and more
                - **Cross-platform**: Works on Windows, Linux, and macOS
                - **Export Capabilities**: Download data in various formats
                
                ### 📊 Visualizations
                
                - Memory usage trends
                - CPU utilization patterns
                - Crash reason distribution
                - Timeline analysis
                - Correlation heatmaps
                - Thread analysis
                """)
            
            with col2:
                st.markdown("""
                ### 🏗️ Architecture
                
                The system uses modern C++17 for the core analysis engine and Python/Streamlit for visualization:
                
                ```mermaid
                graph LR
                    A[C++ Core] --> B[CSV/JSON Export]
                    B --> C[Streamlit Dashboard]
                    C --> D[Interactive Charts]
                    C --> E[Data Analysis] """)