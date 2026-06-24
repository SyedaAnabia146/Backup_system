import streamlit as st
import pandas as pd
from backup_manager import BackupManager

# Basic page layout configuration
st.set_page_config(
    page_title="Automated Backup & Recovery System", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize the backup manager session
if "manager" not in st.session_state:
    st.session_state.manager = BackupManager()

manager = st.session_state.manager

# Custom design styles for a clean light theme layout
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    div[data-testid="stDecoration"] {
        height: 0px !important;
    }
    
    /* Top tabs customization */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important;
        gap: 12px;
        background-color: #E9ECEF;
        padding: 10px;
        border-radius: 12px;
        width: 100% !important;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1 !important;
        text-align: center !important;
        justify-content: center !important;
        height: 48px;
        white-space: nowrap;
        background-color: #FFFFFF;
        border-radius: 8px;
        color: #495057 !important;
        font-weight: 600 !important;
        padding: 0px 15px !important;
        border: 1px solid #DEE2E6;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #0D6EFD !important;
        color: #FFFFFF !important;
        border-color: #0D6EFD;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0D6EFD !important;
        color: #FFFFFF !important;
        border-color: #0D6EFD !important;
        box-shadow: 0px 4px 10px rgba(13, 110, 253, 0.2);
    }
    
    /* Sleek interface buttons */
    .stButton>button, div[data-testid="stForm"] button {
        background-color: #0D6EFD !important;
        color: #FFFFFF !important;
        border: 1px solid #0D6EFD !important;
        border-radius: 6px !important;
        padding: 8px 20px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        width: auto !important;
        max-width: 220px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover, div[data-testid="stForm"] button:hover {
        background-color: #0B5ED7 !important;
    }
    
    /* Custom input field headers */
    .input-label-header {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #495057 !important;
        margin-top: 15px !important;
        margin-bottom: 5px !important;
        text-align: left !important;
    }
    
    /* Dashboard analytics cards */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 13px;
        color: #6C757D;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        color: #0D6EFD;
        font-weight: bold;
    }
    
    /* Header panel design */
    .main-header {
        background: linear-gradient(90deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #1E88E5;
        margin-bottom: 25px;
    }
    .main-header h1 { color: #0D47A1 !important; margin: 0; font-size: 30px; }
    .main-header p { color: #1565C0; margin: 5px 0 0 0; }
    
    .custom-subheader {
        color: #495057;
        font-size: 20px;
        font-weight: 600;
        border-bottom: 2px solid #E9ECEF;
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    
    .bonus-badge {
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        border: 1px solid #A5D6A7;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* High-contrast styling for halt notice */
    .halt-notice {
        background-color: #FDE8E8;
        border: 2px solid #F05252;
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
        color: #C81E1E;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Application Title Block
st.markdown("""
    <div class="main-header">
        <h1>🔄 Automated Data Backup & Recovery System</h1>
        <p>Enterprise-grade secure backup automation, compression management & instant recovery console.</p>
    </div>
""", unsafe_allow_html=True)

# Main Navigation Setup
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard & Logs", 
    "📁 Create Manual Backup", 
    "⏰ Configure Auto Scheduler", 
    "↩️ Restore & Recover Data"
])

# --- TAB 1: SYSTEM ANALYTICS ---
with tab1:
    st.markdown('<div class="custom-subheader">📊 System Analytics & Backup Logs</div>', unsafe_allow_html=True)
    db_history = manager.history
    
    if db_history:
        df = pd.DataFrame(db_history)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">01. Total Attempts</div><div class="metric-value" style="color:#495057;">{len(df)}</div></div>', unsafe_allow_html=True)
        with col2:
            success_count = len(df[df['status'] == 'Success'])
            st.markdown(f'<div class="metric-card"><div class="metric-title">02. Successful Backups</div><div class="metric-value" style="color:#2E7D32;">{success_count}</div></div>', unsafe_allow_html=True)
        with col3:
            storage_used = round(df[df['status'] == 'Success']['size_mb'].sum(), 2)
            st.markdown(f'<div class="metric-card"><div class="metric-title">03. Storage Saved (Compressed)</div><div class="metric-value" style="color:#1565C0;">{storage_used} MB</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No system backup history records are currently available.")

# --- TAB 2: MANUAL BACKUP CONTROL ---
with tab2:
    st.markdown('<span class="bonus-badge">✨ BONUS FEATURE INCLUDED: ZIP COMPRESSION</span>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subheader">📁 Trigger Immediate Manual Backup</div>', unsafe_allow_html=True)
    
    with st.form("backup_form"):
        st.markdown('<div class="input-label-header">SOURCE DIRECTORY (Upload Your Data Path)</div>', unsafe_allow_html=True)
        source_input = st.text_input(
            "Source Input", label_visibility="collapsed",
            placeholder="e.g., C:/Users/project/Backup_System/MyData"
        )
        
        st.markdown('<div class="input-label-header">BACKUP DIRECTORY (Upload Your Backup Path)</div>', unsafe_allow_html=True)
        dest_input = st.text_input(
            "Destination Input", label_visibility="collapsed",
            placeholder="e.g., C:/Users/project/Backup_System/MyBackups"
        )
        
        submit_btn = st.form_submit_button("Execute Backup Job")
        
        if submit_btn:
            if not source_input or not dest_input:
                st.error("Please provide valid source and destination directory paths.")
            else:
                with st.spinner("Creating compressed backup archive..."):
                    result = manager.create_backup(source_input, dest_input, mode="Manual")
                    if result["status"] == "Success":
                        st.success(f"🎉 Backup created successfully! ID: {result['data']['backup_id']} [Compression: ZIP]")
                    else:
                        st.error(f"❌ Backup process failed: {result['message']}")

# --- TAB 3: AUTOMATION SCHEDULER ---
with tab3:
    st.markdown('<span class="bonus-badge">✨ BONUS FEATURE INCLUDED: BACKUP SCHEDULING INTERFACE</span>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subheader">⏰ Background Automation Setup</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-label-header">SOURCE DIRECTORY (Upload Your Data Path)</div>', unsafe_allow_html=True)
    src_schedule = st.text_input(
        "Automation Source Input", label_visibility="collapsed",
        placeholder="e.g., C:/Users/project/Backup_System/MyData"
    )
    
    st.markdown('<div class="input-label-header">BACKUP DIRECTORY (Upload Your Backup Path)</div>', unsafe_allow_html=True)
    dst_schedule = st.text_input(
        "Automation Destination Input", label_visibility="collapsed",
        placeholder="e.g., C:/Users/project/Backup_System/MyBackups"
    )
    
    st.markdown('<div class="input-label-header">TIME FREQUENCY INTERVAL (In Minutes)</div>', unsafe_allow_html=True)
    interval = st.number_input("Interval Input", label_visibility="collapsed", min_value=1, value=5, step=1)
    
    col_start, col_stop = st.columns(2)
    
    with col_start:
        if st.button("Activate Auto Scheduler", use_container_width=False):
            if not src_schedule or not dst_schedule:
                st.error("Both directory paths are required to initialize automation routine.")
            else:
                manager.start_schedule(src_schedule, dst_schedule, interval)
                st.success("🚀 Automation Scheduler initialized! Background routine running.")

    with col_stop:
        if st.button("Deactivate Scheduler", use_container_width=False):
            manager.stop_schedule()
            st.markdown('<div class="halt-notice">🛑 Auto Scheduler background services have been successfully halted.</div>', unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if manager.scheduler_running:
        st.success("🟢 STATUS LOG: Cron-job automated instance currently ACTIVE and running in background.")
    else:
        st.info("⚪ STATUS LOG: Automation scheduler engine is currently IDLE / INACTIVE.")

# --- TAB 4: RECOVERY & RESTORE ---
with tab4:
    st.markdown('<span class="bonus-badge">✨ BONUS FEATURE INCLUDED: INTEGRITY VERIFICATION (CRC32/ZIP CHECK)</span>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subheader">↩️ Disaster Recovery & Decompression Management</div>', unsafe_allow_html=True)
    db_history = manager.history
    
    if not db_history:
        st.warning("No existing backup entries found in the system logs database.")
    else:
        success_backups = [item for item in db_history if item["status"] == "Success"]
        if not success_backups:
            st.error("No valid 'Success' archive version available for system recovery.")
        else:
            backup_options = {f"📦 ID: {item['backup_id']} | Mode: {item['mode']} | Date: {item['date']}" : item['backup_id'] for item in success_backups}
            selected_option = st.selectbox("Select Target Backup Archive Version:", list(backup_options.keys()))
            
            st.markdown('<div class="input-label-header">RESTORE EXTRACTION TARGET PATH (Where to Extract Data)</div>', unsafe_allow_html=True)
            restore_target = st.text_input(
                "Restore Input", label_visibility="collapsed",
                placeholder="e.g., C:/Users/project/Backup_System/RestoredData"
            )
            restore_btn = st.button("Initiate Recovery Routine")
            
            if restore_btn:
                if not restore_target:
                    st.error("Target restoration destination path is mandatory.")
                else:
                    target_id = backup_options[selected_option]
                    with st.spinner("Running Integrity Check & Extracting ZIP archive..."):
                        res = manager.restore_backup(target_id, restore_target)
                        if res["status"] == "Success":
                            st.success(res["message"])
                        else:
                            st.error(res["message"])