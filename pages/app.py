import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth import require_auth, is_authenticated, logout
import streamlit as st

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_auth()

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{
        background: #060916 !important;
        border-right: 1px solid rgba(255,255,255,.07) !important;
    }
    [data-testid="stSidebar"] * { font-family: 'Space Grotesk', sans-serif !important; }
    </style>
    """, unsafe_allow_html=True)

    pic   = st.session_state.get("user_picture", "")
    name  = st.session_state.get("user_name", "User")
    email = st.session_state.get("user_email", "")

    st.markdown(f"""
    <div style="padding:.5rem 0 1rem;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:1.25rem;">
      <div style="display:flex;align-items:center;gap:.85rem;">
        {'<img src="'+pic+'" style="width:42px;height:42px;border-radius:50%;border:2px solid rgba(99,102,241,.4);">' if pic else '<div style="width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#22d3ee);display:flex;align-items:center;justify-content:center;font-size:1.1rem;">👤</div>'}
        <div>
          <div style="font-weight:700;font-size:.9rem;color:#f1f5f9;">{name}</div>
          <div style="font-size:.72rem;color:#64748b;">{email}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.15em;
                  color:#6366f1;text-transform:uppercase;margin-bottom:.6rem;">Pipeline Status</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Logout", use_container_width=True):
        logout()

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:       #03050f;
  --bg2:      #060916;
  --surf:     rgba(255,255,255,.04);
  --surf2:    rgba(255,255,255,.07);
  --border:   rgba(255,255,255,.07);
  --p:        #6366f1;
  --p2:       #818cf8;
  --cyan:     #22d3ee;
  --emerald:  #10b981;
  --amber:    #f59e0b;
  --rose:     #f43f5e;
  --text:     #f1f5f9;
  --muted:    #64748b;
  --muted2:   #94a3b8;
  --display:  'Plus Jakarta Sans', sans-serif;
  --body:     'Space Grotesk', sans-serif;
  --mono:     'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--body) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1180px; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,.35); border-radius: 2px; }

/* ── HERO BANNER ── */
.app-hero {
  background: linear-gradient(135deg, #080d1c 0%, #0d1225 50%, #060916 100%);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 2.5rem 3rem;
  margin-bottom: 2rem;
  position: relative; overflow: hidden;
}
.app-hero::before {
  content: '';
  position: absolute; top: -80px; right: -80px;
  width: 320px; height: 320px; border-radius: 50%;
  background: radial-gradient(circle, rgba(99,102,241,.1), transparent 70%);
  pointer-events: none;
}
.app-hero::after {
  content: '';
  position: absolute; bottom: -60px; left: -40px;
  width: 240px; height: 240px; border-radius: 50%;
  background: radial-gradient(circle, rgba(34,211,238,.06), transparent 70%);
  pointer-events: none;
}
.app-hero-tag {
  display: inline-flex; align-items: center; gap: .4rem;
  font-family: var(--mono); font-size: .62rem; letter-spacing: .18em;
  color: var(--cyan);
  border: 1px solid rgba(34,211,238,.2);
  background: rgba(34,211,238,.06);
  border-radius: 100px; padding: 4px 12px;
  margin-bottom: .9rem;
}
.app-hero h1 {
  font-family: var(--display) !important;
  font-size: 2.4rem !important; font-weight: 800 !important;
  letter-spacing: -.04em !important; line-height: 1.1 !important;
  margin: 0 0 .6rem !important;
  background: linear-gradient(90deg, #f1f5f9 30%, var(--p2)) !important;
  -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
}
.app-hero p {
  color: var(--muted2) !important; font-size: .95rem; line-height: 1.65; margin: 0;
}

/* ── INPUT ── */
.stTextInput > div > div > input {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: .95rem !important;
  padding: .8rem 1rem !important;
  transition: border-color .2s, box-shadow .2s;
}
.stTextInput > div > div > input:focus {
  border-color: var(--p) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important;
}
.stTextInput > label {
  color: var(--muted) !important; font-size: .7rem !important;
  letter-spacing: .12em !important; font-family: var(--mono) !important;
}

/* ── BUTTON ── */
.stButton > button {
  background: linear-gradient(135deg, var(--p), #4338ca) !important;
  color: white !important; border: none !important;
  border-radius: 10px !important;
  font-family: var(--display) !important;
  font-weight: 700 !important; font-size: .88rem !important;
  letter-spacing: .02em !important;
  padding: .72rem 1.8rem !important;
  transition: opacity .2s, transform .15s, box-shadow .2s !important;
  box-shadow: 0 4px 20px rgba(99,102,241,.3) !important;
}
.stButton > button:hover {
  opacity: .9 !important; transform: translateY(-1px) !important;
  box-shadow: 0 8px 28px rgba(99,102,241,.45) !important;
}

/* ── PIPELINE GRID ── */
.pipeline-wrap {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: .9rem; margin-bottom: 1.75rem;
}
.step-card {
  background: var(--surf); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.1rem .9rem;
  text-align: center; position: relative; overflow: hidden;
  transition: border-color .3s, background .3s, transform .2s;
}
.step-card.active {
  border-color: var(--cyan) !important;
  background: rgba(34,211,238,.05) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(34,211,238,.15);
}
.step-card.active::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--cyan), transparent);
  animation: shimmer 1.5s ease infinite;
}
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.step-card.done {
  border-color: var(--emerald) !important;
  background: rgba(16,185,129,.04) !important;
}
.step-card.pending { opacity: .4; }
.step-icon { font-size: 1.5rem; margin-bottom: .4rem; }
.step-num  { font-family: var(--mono); font-size: .58rem; letter-spacing: .1em; color: var(--muted); margin-bottom: .2rem; }
.step-name { font-size: .82rem; font-weight: 700; color: var(--text); }
.step-desc { font-size: .68rem; color: var(--muted); margin-top: 2px; }
.step-badge {
  display: inline-block; font-size: .6rem; font-family: var(--mono);
  border-radius: 4px; padding: 2px 7px; margin-top: .35rem;
  letter-spacing: .05em;
}
.badge-active  { background: rgba(34,211,238,.15); color: var(--cyan); border: 1px solid rgba(34,211,238,.3); }
.badge-done    { background: rgba(16,185,129,.15); color: var(--emerald); border: 1px solid rgba(16,185,129,.3); }
.badge-pending { background: rgba(100,116,139,.1); color: var(--muted); border: 1px solid var(--border); }

/* ── COLLAPSIBLE RESULT SECTIONS ── */
.result-wrap {
  background: var(--surf);
  border: 1px solid var(--border);
  border-radius: 14px;
  margin-bottom: 1rem;
  overflow: hidden;
  transition: border-color .25s, box-shadow .25s;
}
.result-wrap.open { border-color: rgba(99,102,241,.3); }
.result-wrap:hover { box-shadow: 0 4px 24px rgba(0,0,0,.3); }

.result-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 1.6rem;
  cursor: pointer;
  user-select: none;
  transition: background .2s;
}
.result-header:hover { background: rgba(255,255,255,.025); }

.result-header-left { display: flex; align-items: center; gap: .9rem; }
.result-header-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; flex-shrink: 0;
}
.icon-search   { background: linear-gradient(135deg,rgba(34,211,238,.2),rgba(34,211,238,.05)); border:1px solid rgba(34,211,238,.2); }
.icon-reader   { background: linear-gradient(135deg,rgba(99,102,241,.2),rgba(99,102,241,.05)); border:1px solid rgba(99,102,241,.2); }
.icon-writer   { background: linear-gradient(135deg,rgba(244,63,94,.2),rgba(244,63,94,.05)); border:1px solid rgba(244,63,94,.2); }
.icon-critic   { background: linear-gradient(135deg,rgba(245,158,11,.2),rgba(245,158,11,.05)); border:1px solid rgba(245,158,11,.2); }

.result-header-meta {}
.result-header-tag {
  font-family: var(--mono); font-size: .58rem; letter-spacing: .15em;
  color: var(--muted); text-transform: uppercase; margin-bottom: .15rem;
}
.result-header-title { font-family: var(--display); font-size: .95rem; font-weight: 700; color: var(--text); }
.result-chevron {
  font-size: .75rem; color: var(--muted); transition: transform .3s;
  flex-shrink: 0; margin-left: 1rem;
}
.result-chevron.open { transform: rotate(180deg); }

.result-body-wrap {
  border-top: 1px solid var(--border);
  padding: 1.4rem 1.6rem;
}
.result-content {
  font-size: .85rem; line-height: 1.78;
  color: #94a3b8; font-family: var(--mono);
  white-space: pre-wrap; word-break: break-word;
  max-height: 400px; overflow-y: auto;
}
.result-content-report {
  font-family: var(--body) !important;
  font-size: .92rem !important; line-height: 1.82 !important;
  color: var(--text) !important;
  white-space: pre-wrap; word-break: break-word;
  max-height: 500px; overflow-y: auto;
}
.result-content-feedback {
  font-family: var(--body) !important;
  font-size: .9rem !important; line-height: 1.8 !important;
  color: var(--muted2) !important;
  white-space: pre-wrap; word-break: break-word;
  max-height: 400px; overflow-y: auto;
}

/* ── STATUS BAR ── */
.status-complete {
  display: flex; align-items: center; gap: .75rem;
  background: rgba(16,185,129,.06);
  border: 1px solid rgba(16,185,129,.2);
  border-radius: 10px; padding: .85rem 1.2rem;
  margin-bottom: 1.5rem;
}
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 8px var(--emerald); }
.status-text { font-family: var(--mono); font-size: .7rem; letter-spacing: .1em; color: var(--emerald); }

/* ── ERROR ── */
.error-box {
  background: rgba(244,63,94,.07);
  border: 1px solid rgba(244,63,94,.25);
  border-radius: 10px; padding: 1.1rem 1.4rem;
  color: #fca5a5; font-family: var(--mono); font-size: .82rem;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--p) !important; }

/* ── DOWNLOAD BTN ── */
.stDownloadButton > button {
  background: var(--surf2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  font-family: var(--body) !important;
  font-weight: 600 !important;
  transition: background .2s, border-color .2s !important;
}
.stDownloadButton > button:hover {
  background: rgba(99,102,241,.12) !important;
  border-color: rgba(99,102,241,.4) !important;
}

hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_text(result) -> str:
    if isinstance(result, str): return result
    if hasattr(result, "content"):
        c = result.content
        if isinstance(c, list):
            return "\n".join(b if isinstance(b, str) else b.get("text", "") for b in c if isinstance(b, (str, dict)))
        return str(c)
    if isinstance(result, list):
        return extract_text(result[-1]) if result else ""
    if isinstance(result, dict):
        for k in ("content", "text"):
            if k in result: return extract_text(result[k])
        if "messages" in result and result["messages"]:
            return extract_text(result["messages"][-1])
    return str(result)


STEPS = [
    ("🔍", "STEP 01", "Search Agent",  "Fetching live data"),
    ("📄", "STEP 02", "Reader Agent",  "Scraping top URLs"),
    ("✍️",  "STEP 03", "Writer Chain", "Drafting report"),
    ("🧠", "STEP 04", "Critic Chain",  "Reviewing report"),
]

def render_pipeline(active=-1, done_up_to=-1):
    cards = ""
    for i, (icon, label, name, desc) in enumerate(STEPS):
        if   i == active:      sc, bc, bt = "active",  "badge-active",  "● RUNNING"
        elif i <= done_up_to:  sc, bc, bt = "done",    "badge-done",    "✓ DONE"
        else:                  sc, bc, bt = "pending",  "badge-pending", "WAITING"
        cards += f"""<div class="step-card {sc}">
            <div class="step-icon">{icon}</div>
            <div class="step-num">{label}</div>
            <div class="step-name">{name}</div>
            <div class="step-desc">{desc}</div>
            <span class="step-badge {bc}">{bt}</span>
        </div>"""
    st.markdown(f'<div class="pipeline-wrap">{cards}</div>', unsafe_allow_html=True)


def collapsible_result(key, icon, icon_cls, tag, title, body, content_cls="result-content", default_open=False):
    """Renders a collapsible result section using session state."""
    import html as _h
    state_key = f"open_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = default_open

    is_open = st.session_state[state_key]
    chevron_cls = "open" if is_open else ""
    wrap_cls    = "open" if is_open else ""
    safe_body   = _h.escape(str(body))

    # Header acts as toggle button
    col1, col2 = st.columns([20, 1])
    with col1:
        st.markdown(f"""
        <div class="result-wrap {wrap_cls}">
          <div class="result-header" id="hdr_{key}">
            <div class="result-header-left">
              <div class="result-header-icon {icon_cls}">{icon}</div>
              <div class="result-header-meta">
                <div class="result-header-tag">{tag}</div>
                <div class="result-header-title">{title}</div>
              </div>
            </div>
            <div class="result-chevron {chevron_cls}">▼</div>
          </div>
          {'<div class="result-body-wrap"><div class="' + content_cls + '">' + safe_body + '</div></div>' if is_open else ''}
        </div>
        """, unsafe_allow_html=True)

    # Toggle button (invisible, aligned with chevron)
    with col2:
        label = "▲" if is_open else "▼"
        if st.button(label, key=f"btn_{key}", help="Toggle section"):
            st.session_state[state_key] = not is_open
            st.rerun()


# ── Hero ──────────────────────────────────────────────────────────────────────
user_name = st.session_state.get("user_name", "")
st.markdown(f"""
<div class="app-hero">
  <div class="app-hero-tag">
    <span style="width:6px;height:6px;border-radius:50%;background:var(--cyan);display:inline-block;animation:blink 2s ease infinite;"></span>
    MULTI-AGENT · AI-POWERED
  </div>
  <h1>ResearchMind</h1>
  <p>Welcome back, <strong style="color:#f1f5f9;">{user_name}</strong> — 
  Enter a topic below to trigger the 4-stage autonomous research pipeline.</p>
</div>
<style>@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:.2;}}}}</style>
""", unsafe_allow_html=True)

# ── Input Row ────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_in:
    topic = st.text_input(
        "RESEARCH TOPIC",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        key="topic_input",
    )
with col_btn:
    run_btn = st.button("▶  Run", use_container_width=True)

st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# ── Run Pipeline ─────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown('<div class="error-box">⚠ Please enter a research topic before running.</div>', unsafe_allow_html=True)
        st.stop()

    step_ph   = st.empty()
    status_ph = st.empty()

    try:
        state = {}

        # Step 1
        with step_ph.container(): render_pipeline(active=0, done_up_to=-1)
        with status_ph.container():
            with st.spinner("🔍  Search Agent is fetching live data…"):
                state["search_results"] = extract_text(build_search_agent().invoke({
                    "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
                }))

        # Step 2
        with step_ph.container(): render_pipeline(active=1, done_up_to=0)
        with status_ph.container():
            with st.spinner("📄  Reader Agent is scraping top resources…"):
                state["scraped_content"] = extract_text(build_reader_agent().invoke({
                    "messages": [("user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}")]
                }))

        # Step 3
        with step_ph.container(): render_pipeline(active=2, done_up_to=1)
        with status_ph.container():
            with st.spinner("✍️  Writer Chain is drafting the report…"):
                state["report"] = extract_text(writer_chain.invoke({
                    "topic": topic,
                    "research": f"SEARCH RESULTS:\n{state['search_results']}\n\nSCRAPED CONTENT:\n{state['scraped_content']}"
                }))

        # Step 4
        with step_ph.container(): render_pipeline(active=3, done_up_to=2)
        with status_ph.container():
            with st.spinner("🧠  Critic Chain is reviewing the report…"):
                state["feedback"] = extract_text(critic_chain.invoke({"report": state["report"]}))

        # Done
        with step_ph.container(): render_pipeline(active=-1, done_up_to=3)
        status_ph.empty()

        # Store in session so collapsibles persist
        st.session_state["last_state"] = state
        st.session_state["last_topic"] = topic

        # Open writer and critic by default, keep others closed
        st.session_state["open_search"]  = False
        st.session_state["open_reader"]  = False
        st.session_state["open_writer"]  = True
        st.session_state["open_critic"]  = True

    except Exception as e:
        step_ph.empty(); status_ph.empty()
        st.markdown(f'<div class="error-box">❌ Pipeline error: {e}</div>', unsafe_allow_html=True)

# ── Show results (persists across reruns via session_state) ───────────────────
if "last_state" in st.session_state:
    state = st.session_state["last_state"]
    topic = st.session_state.get("last_topic", "")

    st.markdown("""
    <div class="status-complete">
      <div class="status-dot"></div>
      <div class="status-text">PIPELINE COMPLETE — 4 / 4 STAGES FINISHED — Click any section to expand or collapse</div>
    </div>
    """, unsafe_allow_html=True)

    collapsible_result(
        "search", "🔍", "icon-search",
        "STAGE 01 · SEARCH AGENT", "Raw Search Results",
        state["search_results"],
        content_cls="result-content",
        default_open=False,
    )
    collapsible_result(
        "reader", "📄", "icon-reader",
        "STAGE 02 · READER AGENT", "Scraped Web Content",
        state["scraped_content"],
        content_cls="result-content",
        default_open=False,
    )
    collapsible_result(
        "writer", "✍️", "icon-writer",
        "STAGE 03 · WRITER CHAIN", "Generated Research Report",
        state["report"],
        content_cls="result-content-report",
        default_open=True,
    )
    collapsible_result(
        "critic", "🧠", "icon-critic",
        "STAGE 04 · CRITIC CHAIN", "Expert Feedback & Review",
        state["feedback"],
        content_cls="result-content-feedback",
        default_open=True,
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    full_output = (
        f"TOPIC: {topic}\n{'='*60}\n\n"
        f"[SEARCH RESULTS]\n{state['search_results']}\n\n"
        f"[SCRAPED CONTENT]\n{state['scraped_content']}\n\n"
        f"[REPORT]\n{state['report']}\n\n"
        f"[CRITIC FEEDBACK]\n{state['feedback']}\n"
    )
    st.download_button(
        label="⬇  Download Full Report (.txt)",
        data=full_output,
        file_name=f"research_{topic[:40].replace(' ','_')}.txt",
        mime="text/plain",
    )

elif not run_btn:
    render_pipeline(active=-1, done_up_to=-1)
    st.markdown("""
    <p style="text-align:center;color:var(--muted);font-family:'JetBrains Mono',monospace;
              font-size:.72rem;letter-spacing:.1em;margin-top:.5rem;padding-bottom:2rem;">
      ENTER A TOPIC ABOVE AND CLICK RUN TO START THE PIPELINE
    </p>
    """, unsafe_allow_html=True)