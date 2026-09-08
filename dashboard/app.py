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
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stApp { background-color: #1e1e1e; color: #cccccc; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 2px solid #ffffff !important; }
    [data-testid="stSidebar"] * { color: #ffffff; }
    
    .sidebar-new-btn > button { background-color: #222222 !important; border: 1px solid #ffffff !important; border-radius: 5px !important; margin-bottom: 20px; }
    .sidebar-new-btn > button:hover { background-color: #444444 !important; }
    
    .main-title { font-size: 2.2rem; font-weight: 600; color: #ffffff; margin-bottom: 5px; }
    .sub-title { font-size: 1rem; color: #9cdcfe; margin-bottom: 30px; }

    .stTextArea textarea, .stTextInput input {
        background-color: #252526 !important; border: 1px solid #3c3c3c !important;
        border-radius: 3px !important; color: #cccccc !important; padding: 10px !important; box-shadow: none !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus { border-color: #007fd4 !important; background-color: #2d2d2d !important; }
    label, .stMarkdown p { color: #cccccc !important; font-size: 0.9rem !important; font-weight: 400 !important; }
    
    /* Main Action Button */
    .primary-btn > div[data-testid="stButton"] > button {
        background-color: #0e639c !important; border: 1px solid transparent !important;
        border-radius: 2px !important; color: #ffffff !important; font-weight: 600 !important;
        padding: 10px 16px !important; transition: background-color 0.1s ease !important;
    }
    .primary-btn > div[data-testid="stButton"] > button:hover { background-color: #1177bb !important; }
    
    /* Approve Button */
    .approve-btn > div[data-testid="stButton"] > button {
        background-color: #238636 !important; border: 1px solid rgba(240,246,252,0.1) !important;
        color: #ffffff !important; font-weight: 600 !important;
    }
    .approve-btn > div[data-testid="stButton"] > button:hover { background-color: #2ea043 !important; }
    
    /* Reject Button */
    .reject-btn > div[data-testid="stButton"] > button {
        background-color: #da3633 !important; border: 1px solid rgba(240,246,252,0.1) !important;
        color: #ffffff !important; font-weight: 600 !important;
    }
    .reject-btn > div[data-testid="stButton"] > button:hover { background-color: #f85149 !important; }

    div[data-testid="stCodeBlock"] { background-color: #1e1e1e !important; border: 1px solid #454545 !important; border-radius: 3px !important; }
    div[data-testid="stCodeBlock"] code { color: #cccccc !important; font-family: Consolas, "Courier New", monospace !important; font-size: 0.9rem !important; }
    
    .approval-card {
        background-color: #252526; border: 1px solid #007fd4; border-radius: 5px;
        padding: 20px; margin-top: 20px; border-left: 5px solid #007fd4;
    }
</style>
""", unsafe_allow_html=True)

_DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_DASHBOARD_DIR)
_TASKS_DIR = os.path.join(_DASHBOARD_DIR, "tasks")

if "form_reset_counter" not in st.session_state:
    st.session_state.form_reset_counter = 0

# --- SIDEBAR LOGIC ---
with st.sidebar:
    st.markdown("<h2>History</h2>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-new-btn">', unsafe_allow_html=True)
    if st.button("📝 New chat (Reset)", use_container_width=True):
        st.session_state.form_reset_counter += 1
        st.session_state.selected_task_file = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Recents")
    task_files = glob.glob(os.path.join(_TASKS_DIR, "*.json"))
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
                t_status = data.get("status", "")
                
                # Truncate description for sidebar
                if len(t_req) > 35:
                    t_req = t_req[:32] + "..."
                    
                # 2-column layout for the history item and the delete button
                scol1, scol2 = st.columns([4, 1])
                with scol1:
                    icon = "👀" if t_status == "awaiting_human_approval" else "✅" if t_status in ("approved", "verified_fixed") else "📄"
                    if st.button(f"{icon} {t_id}\n{t_req}", key=f"sel_{t_id}", use_container_width=True):
                        st.session_state.selected_task_file = f
                        st.rerun()
                with scol2:
                    if st.button("🗑️", key=f"del_{t_id}"):
                        os.remove(f)
                        if st.session_state.get("selected_task_file") == f:
                            st.session_state.selected_task_file = None
                        st.rerun()
            except Exception as e:
                pass

# Load selected task data if present
loaded_req = ""
loaded_repo = "sample_repo/flaskbb"
loaded_tid = f"live_{int(time.time()) % 1000:03d}"
loaded_diff = None
loaded_plan = None

if st.session_state.get("selected_task_file") and os.path.exists(st.session_state.selected_task_file):
    try:
        with open(st.session_state.selected_task_file, "r", encoding="utf-8") as f_in:
            sel_data = json.load(f_in)
            loaded_req = sel_data.get("feature_request", "")
            loaded_tid = sel_data.get("task_id", "")
            loaded_diff = sel_data.get("code_diff")
            loaded_plan = sel_data.get("plan")
    except Exception:
        pass


# --- MAIN CONTENT ---
st.markdown("<div class='main-title'>🤖 AI DEV TEAM</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>A MULTI AGENT MODEL FOR DEALING WITH PYTHON PROJECTS</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, spacer, col2 = st.columns([2.5, 0.2, 1])
key_suffix = st.session_state.form_reset_counter

with col1:
    st.markdown("<p><b>ENTER REQUESTS:-</b></p>", unsafe_allow_html=True)
    user_request = st.text_area("Request", key=f"req_{key_suffix}", label_visibility="collapsed", value=loaded_req, placeholder="create a testers.py that prints hi", height=140)

with col2:
    st.markdown("<p><b>project directory</b></p>", unsafe_allow_html=True)
    target_repo = st.text_input("Repo", key=f"repo_{key_suffix}", label_visibility="collapsed", value=loaded_repo)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("<p><b>Task-ID (optional):</b></p>", unsafe_allow_html=True)
    task_id = st.text_input("Task", key=f"task_{key_suffix}", label_visibility="collapsed", value=loaded_tid)

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

# Run Button
st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
if st.button("🚀 RUN PIPELINE", use_container_width=True):
    tid_clean = task_id.strip()
    task_file_path = os.path.join(_TASKS_DIR, f"{tid_clean}.json") if tid_clean else None
    
    if not user_request.strip():
        st.error("Please enter a feature request first.")
    elif task_file_path and os.path.exists(task_file_path):
        st.error(f"Task ID `{tid_clean}` already exists. Please choose a different Task ID or click 'New chat' to auto-generate one.")
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
                cmd, cwd=_REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, encoding="utf-8", errors="replace"
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
            
st.markdown('</div>', unsafe_allow_html=True)

# Display historical data if selected
if loaded_diff or loaded_plan:
    st.markdown("---")
    st.markdown(f"### 🕒 History for Task: `{loaded_tid}`")
    
    tab1, tab2 = st.tabs(["💻 Code Diff", "📋 Architect Plan"])
    
    with tab1:
        if loaded_diff:
            st.code(loaded_diff, language="diff")
        else:
            st.info("No code changes were generated for this task.")
            
    with tab2:
        if loaded_plan:
            st.markdown(loaded_plan)
        else:
            st.info("No architectural plan was generated.")

# --- HUMAN APPROVAL SECTION ---
pending_tasks = []
for f in task_files:
    try:
        with open(f, "r", encoding="utf-8") as f_in:
            data = json.load(f_in)
            if data.get("status") == "awaiting_human_approval" and data.get("code_diff"):
                pending_tasks.append((f, data))
    except Exception:
        pass

if pending_tasks:
    st.markdown("---")
    st.markdown("### 👀 Pending Human Approvals")
    
    for f_path, t_data in pending_tasks:
        tid = t_data.get("task_id", "Unknown")
        freq = t_data.get("feature_request", "")
        diff = t_data.get("code_diff", "")
        
        st.markdown(f"""
        <div class="approval-card">
            <h4>Task: {tid}</h4>
            <p><i>{freq}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code(diff, language="diff")
        
        acol1, acol2, _ = st.columns([1, 1, 4])
        
        with acol1:
            st.markdown('<div class="approve-btn">', unsafe_allow_html=True)
            if st.button("✅ Approve & Apply", key=f"approve_{tid}"):
                t_data["status"] = "approved"
                with open(f_path, "w", encoding="utf-8") as f_out:
                    json.dump(t_data, f_out, indent=2)
                
                st.info(f"Applying fixes for task {tid}...")
                apply_cmd = [sys.executable, "orchestration/apply_fixes.py", "--repo", target_repo]
                try:
                    res = subprocess.run(apply_cmd, cwd=_REPO_ROOT, capture_output=True, text=True)
                    if res.returncode == 0:
                        st.success(f"Changes applied successfully!\n\n{res.stdout}")
                        st.rerun()
                    else:
                        st.error(f"Failed to apply fixes:\n{res.stderr}")
                except Exception as e:
                    st.error(f"Error executing apply_fixes.py: {e}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with acol2:
            st.markdown('<div class="reject-btn">', unsafe_allow_html=True)
            if st.button("❌ Reject", key=f"reject_{tid}"):
                t_data["status"] = "rejected"
                with open(f_path, "w", encoding="utf-8") as f_out:
                    json.dump(t_data, f_out, indent=2)
                st.warning(f"Task {tid} rejected.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
