import sys
import os
import time
import subprocess
import glob
import json
import streamlit as st

st.set_page_config(page_title="AI Dev Team", page_icon="🤖", layout="wide")

# VS Code Dark+ Theme CSS + Sidebar Styles
st.markdown("""
<style>
    /* Global VS Code Font */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main Background (VS Code Editor Background) */
    .stApp {
        background-color: #1e1e1e;
        color: #cccccc;
    }
    
    /* Sidebar Styling - Black with White Border */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 2px solid #ffffff !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff;
    }
    
    /* Custom Sidebar New Task Button */
    .sidebar-new-btn > button {
        background-color: #222222 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
        margin-bottom: 20px;
    }
    .sidebar-new-btn > button:hover {
        background-color: #444444 !important;
    }
    
    /* Main Title */
    .main-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .sub-title {
        font-size: 1rem;
        color: #9cdcfe; /* VS Code light blue variable color */
        margin-bottom: 30px;
    }

    /* Inputs (Text Area and Text Input) */
    .stTextArea textarea, .stTextInput input {
        background-color: #252526 !important;
        border: 1px solid #3c3c3c !important;
        border-radius: 3px !important;
        color: #cccccc !important;
        font-size: 0.95rem !important;
        padding: 10px !important;
        box-shadow: none !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #007fd4 !important;
        box-shadow: none !important;
        background-color: #2d2d2d !important;
    }
    
    /* Labels */
    label, .stMarkdown p {
        color: #cccccc !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
    }
    
    /* Main Action Button */
    div[data-testid="stButton"] > button {
        background-color: #0e639c !important; 
        border: 1px solid transparent !important;
        border-radius: 2px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 10px 16px !important;
        transition: background-color 0.1s ease !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #1177bb !important;
        border-color: transparent !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stButton"] > button:active {
        background-color: #094771 !important;
    }

    /* Terminal Output Code Block */
    div[data-testid="stCodeBlock"] {
        background-color: #1e1e1e !important;
        border: 1px solid #454545 !important;
        border-radius: 3px !important;
    }
    
    div[data-testid="stCodeBlock"] code {
        color: #cccccc !important;
        font-family: Consolas, "Courier New", monospace !important;
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_DASHBOARD_DIR)
_TASKS_DIR = os.path.join(_DASHBOARD_DIR, "tasks")

# Session state for clearing form
if "form_reset_counter" not in st.session_state:
    st.session_state.form_reset_counter = 0

# --- SIDEBAR LOGIC ---
with st.sidebar:
    st.markdown("<h2>ChatGPT Style History</h2>", unsafe_allow_html=True)
    
    # New Task Button
    st.markdown('<div class="sidebar-new-btn">', unsafe_allow_html=True)
    if st.button("📝 New chat (Reset)", use_container_width=True):
        st.session_state.form_reset_counter += 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Recents")
    
    # Load past tasks
    task_files = glob.glob(os.path.join(_TASKS_DIR, "*.json"))
    
    # Sort files by creation time descending (newest first)
    task_files.sort(key=os.path.getctime, reverse=True)
    
    if not task_files:
        st.caption("No history yet.")
    else:
        for f in task_files:
            try:
                with open(f, "r", encoding="utf-8") as f_in:
                    data = json.load(f_in)
                    t_id = data.get("task_id", os.path.basename(f))
                    t_req = data.get("feature_request", "No description")
                    
                    # Truncate description for sidebar
                    if len(t_req) > 35:
                        t_req = t_req[:32] + "..."
                        
                    # 2-column layout for the history item and the delete button
                    scol1, scol2 = st.columns([4, 1])
                    with scol1:
                        st.markdown(f"**{t_id}**<br><span style='font-size:0.8em;'>{t_req}</span>", unsafe_allow_html=True)
                    with scol2:
                        # Trash icon to delete
                        if st.button("🗑️", key=f"del_{t_id}"):
                            os.remove(f)
                            st.rerun()
            except Exception:
                pass


# --- MAIN CONTENT ---
st.markdown("<div class='main-title'>🤖 AI DEV TEAM</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>A MULTI AGENT MODEL FOR DEALING WITH PYTHON PROJECTS</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, spacer, col2 = st.columns([2.5, 0.2, 1])

# Use reset counter to clear default values if "New Chat" was pressed
key_suffix = st.session_state.form_reset_counter

with col1:
    st.markdown("<p><b>ENTER REQUESTS:-</b></p>", unsafe_allow_html=True)
    user_request = st.text_area("Request", key=f"req_{key_suffix}", label_visibility="collapsed", placeholder="create a testers.py that prints hi", height=140)

with col2:
    st.markdown("<p><b>project directory</b></p>", unsafe_allow_html=True)
    target_repo = st.text_input("Repo", key=f"repo_{key_suffix}", label_visibility="collapsed", value="sample_repo/flaskbb")
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("<p><b>Task-ID (optional):</b></p>", unsafe_allow_html=True)
    task_id = st.text_input("Task", key=f"task_{key_suffix}", label_visibility="collapsed", value=f"live_{int(time.time()) % 1000:03d}")

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

# Run Button
if st.button("🚀 RUN PIPELINE", use_container_width=True):
    if not user_request.strip():
        st.error("Please enter a feature request first.")
    else:
        st.info(f"Running command: `python orchestration/pipeline.py --repo {target_repo} --request \"...\"`")
        
        cmd = [
            sys.executable, "-u", "orchestration/pipeline.py",
            "--repo", target_repo,
            "--request", user_request.strip()
        ]
        
        if task_id.strip():
            cmd.extend(["--task-id", task_id.strip()])

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        log_box = st.empty()
        captured_lines = []

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=_REPO_ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding="utf-8",
                errors="replace",
            )

            if proc.stdout:
                for line in iter(proc.stdout.readline, ""):
                    captured_lines.append(line)
                    display_text = "".join(captured_lines[-40:])
                    log_box.code(display_text, language="shell")

            proc.wait()

            if proc.returncode == 0:
                st.success("✅ Pipeline completed successfully!")
            else:
                st.error("❌ Pipeline finished with an error. Check the logs above.")

        except Exception as e:
            st.error(f"Failed to start pipeline: {e}")
