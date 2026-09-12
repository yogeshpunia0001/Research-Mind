import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Mind · AI Research Agent",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base (Half Top Margin) ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #ffffff;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { 
    padding-top: 1rem !important; /* Cut top space in half */
    padding-bottom: 3rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1100px; 
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 0.8rem 0 1rem; /* Compact padding */
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 0.4rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 0.6rem;
}
.hero h1 span {
    color: #ff8c32;
}
.hero-sub {
    font-size: 1rem;
    font-weight: 400;
    color: #a09890;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.55;
    text-align: center;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.25), transparent);
    margin: 1.4rem 0;
}

/* ── Input Box: Crisp White BG & Light Gray Placeholder ── */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid rgba(255,140,50,0.35) !important;
    border-radius: 10px !important;
    color: #111111 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.2s ease-in-out !important;
}
.stTextInput > div > div > input::placeholder {
    color: #888888 !important;
    opacity: 1 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.2) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 600 !important;
    margin-bottom: 0.3rem !important;
}

/* ── Action Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 18px rgba(255,140,50,0.3) !important;
    width: 100%;
}
.stButton > button:disabled {
    background: rgba(255,255,255,0.08) !important;
    color: #666666 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}

/* ── Horizontal Pipeline Cards ── */
.pipeline-row-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #888888;
    margin: 1.4rem 0 0.6rem;
}

.step-card {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1rem 0.9rem;
    min-height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s ease;
}
.step-card.active {
    border-color: #ff8c32 !important;
    background: rgba(255, 140, 50, 0.08) !important;
    box-shadow: 0 0 16px rgba(255, 140, 50, 0.22) !important;
}
.step-card.done {
    border-color: rgba(80, 200, 120, 0.5) !important;
    background: rgba(80, 200, 120, 0.04) !important;
}
.step-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    color: #ff8c32;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-desc {
    font-size: 0.74rem;
    color: #858078;
    line-height: 1.35;
}
.step-status-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    padding: 2px 6px;
    border-radius: 4px;
}
.status-waiting  { color: #555555; background: rgba(255,255,255,0.03); }
.status-running  { color: #ff8c32; background: rgba(255,140,50,0.18); animation: pulse 1.5s infinite; }
.status-done     { color: #50c878; background: rgba(80,200,120,0.18); }

@keyframes pulse {
    0% { opacity: 0.5; }
    50% { opacity: 1; }
    100% { opacity: 0.5; }
}

/* ── Status Indicator Dark Styling (st.status Override) ── */
div[data-testid="stStatusWidget"], details[data-testid="stExpander"] {
    background: #111116 !important;
    border: 1px solid rgba(255, 140, 50, 0.3) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}
div[data-testid="stStatusWidget"] summary, details[data-testid="stExpander"] summary {
    color: #ffc83b !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── Vibrant Output Containers & High Specificity Typography ── */
.report-box {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 140, 50, 0.4);
    border-radius: 14px;
    padding: 2rem 2.2rem;
    margin-top: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.feedback-box {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(80, 200, 120, 0.4);
    border-radius: 14px;
    padding: 1.8rem 2.2rem;
    margin-top: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
.panel-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding-bottom: 0.7rem;
    margin-bottom: 1.4rem;
}
.panel-header.orange {
    color: #ff8c32;
    border-bottom: 1px solid rgba(255,140,50,0.25);
}
.panel-header.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80,200,120,0.25);
}

/* ── Force Vibrant Visibility Over Streamlit Markdown ── */
.report-box div[data-testid="stMarkdownContainer"] *,
.report-box p,
.report-box li,
.report-box span {
    color: #ffffff !important;
    font-size: 0.98rem !important;
    line-height: 1.85 !important;
}

.report-box div[data-testid="stMarkdownContainer"] h1,
.report-box div[data-testid="stMarkdownContainer"] h2,
.report-box div[data-testid="stMarkdownContainer"] h3,
.report-box div[data-testid="stMarkdownContainer"] h4 {
    font-family: 'Syne', sans-serif !important;
    color: #ffc83b !important; /* Rich Golden Yellow Headers */
    margin-top: 1.6rem !important;
    margin-bottom: 0.6rem !important;
}

.report-box div[data-testid="stMarkdownContainer"] strong,
.report-box div[data-testid="stMarkdownContainer"] b {
    color: #ff9d42 !important; /* Glowing Neon Amber Accent */
    font-weight: 600 !important;
}

.report-box table {
    width: 100%;
    margin: 1.2rem 0;
    border-collapse: collapse;
}
.report-box th {
    background: rgba(255, 140, 50, 0.18) !important;
    color: #ffc83b !important;
    padding: 0.7rem 1rem !important;
    border: 1px solid rgba(255, 140, 50, 0.35) !important;
}
.report-box td {
    padding: 0.7rem 1rem !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
}

.feedback-box div[data-testid="stMarkdownContainer"] * {
    color: #ffffff !important;
    font-size: 0.96rem !important;
    line-height: 1.8 !important;
}
.feedback-box div[data-testid="stMarkdownContainer"] strong {
    color: #50c878 !important;
}

.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #777777;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Session State Initialization ─────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "current_step" not in st.session_state:
    st.session_state.current_step = None


# ── Step Card Renderer ────────────────────────────────────────────────────────
def render_step_card(col, num, title, desc, step_key):
    r = st.session_state.results
    is_running = st.session_state.running
    curr = st.session_state.current_step

    if step_key in r:
        label, status_cls, card_cls = "✓ DONE", "status-done", "done"
    elif is_running and curr == step_key:
        label, status_cls, card_cls = "● WORKING", "status-running", "active"
    else:
        label, status_cls, card_cls = "IDLE", "status-waiting", ""

    col.markdown(f"""
    <div class="step-card {card_cls}">
        <div>
            <div class="step-top">
                <span class="step-num">{num}</span>
                <span class="step-status-tag {status_cls}">{label}</span>
            </div>
            <div class="step-title">{title}</div>
        </div>
        <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Autonomous Multi-Agent System</div>
    <h1>Research <span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, synthesizing,
        and evaluating — to generate deep, grounded research reports.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Search Input & Action Button ──────────────────────────────────────────────
topic = st.text_input(
    "Enter Research Topic",
    placeholder="e.g. Next-generation solid-state battery breakthroughs in 2026",
    key="topic_input",
    disabled=st.session_state.running,
    label_visibility="visible",
)

btn_label = "⏳ Running Autonomous Pipeline..." if st.session_state.running else "⚡  Run Research Pipeline"
run_btn = st.button(btn_label, use_container_width=True, disabled=st.session_state.running)


# ── Horizontal Pipeline Steps ─────────────────────────────────────────────────
st.markdown('<div class="pipeline-row-title">Pipeline Workflow</div>', unsafe_allow_html=True)
p_col1, p_col2, p_col3, p_col4 = st.columns(4)

render_step_card(p_col1, "01", "Search Agent", "Discovers real-time web sources", "search")
render_step_card(p_col2, "02", "Reader Agent", "Scrapes & extracts core content", "reader")
render_step_card(p_col3, "03", "Writer Chain", "Drafts detailed structured report", "writer")
render_step_card(p_col4, "04", "Critic Chain", "Scores & provides critical review", "critic")


# ── Sequential Execution Loop (Smooth 1-by-1 Step Activation) ─────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.current_step = "search"
        st.rerun()

if st.session_state.running:
    topic_val = st.session_state.topic_input
    results = dict(st.session_state.results)

    # ── Stage 1: Search ──
    if st.session_state.current_step == "search":
        with st.status("🔍 Step 1/4: Search Agent is querying live web sources...", expanded=True) as status:
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable, and detailed information about: {topic_val}")]
            })
            results["search"] = sr["messages"][-1].content
            st.session_state.results = results
            st.session_state.current_step = "reader"  # Move to next step
            status.update(label="✓ Step 1/4: Web search completed", state="complete")
        time.sleep(0.5)
        st.rerun()

    # ── Stage 2: Reader ──
    elif st.session_state.current_step == "reader":
        with st.status("📄 Step 2/4: Reader Agent is parsing & scraping primary URLs...", expanded=True) as status:
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = rr["messages"][-1].content
            st.session_state.results = results
            st.session_state.current_step = "writer"  # Move to next step
            status.update(label="✓ Step 2/4: Web scraping completed", state="complete")
        time.sleep(0.5)
        st.rerun()

    # ── Stage 3: Writer ──
    elif st.session_state.current_step == "writer":
        with st.status("✍️ Step 3/4: Writer is synthesizing and drafting research report...", expanded=True) as status:
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined
            })
            st.session_state.results = results
            st.session_state.current_step = "critic"  # Move to next step
            status.update(label="✓ Step 3/4: Report synthesized", state="complete")
        time.sleep(0.5)
        st.rerun()

    # ── Stage 4: Critic ──
    elif st.session_state.current_step == "critic":
        with st.status("🧐 Step 4/4: Critic is evaluating and scoring report quality...", expanded=True) as status:
            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })
            st.session_state.results = results
            st.session_state.running = False
            st.session_state.current_step = None
            status.update(label="✓ Step 4/4: Research review completed", state="complete")
        st.rerun()


# ── Results Presentation ──────────────────────────────────────────────────────
r = st.session_state.results

if r and not st.session_state.running:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family: \'Syne\', sans-serif; font-size: 1.35rem; font-weight: 700; color: #f0ebe0; margin-bottom: 0.8rem;">Synthesized Findings</div>', unsafe_allow_html=True)

    # Raw inspection expanders
    if "search" in r:
        with st.expander("🔍 Inspect Search Agent Raw Findings", expanded=False):
            st.markdown(r["search"])

    if "reader" in r:
        with st.expander("📄 Inspect Scraped Page Context", expanded=False):
            st.markdown(r["reader"])

    # Final Synthesized Report with Vibrant Text Wrapping
    if "writer" in r:
        st.markdown("""
        <div class="report-box">
            <div class="panel-header orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Critic evaluation
    if "critic" in r:
        st.markdown("""
        <div class="feedback-box">
            <div class="panel-header green">🧐 Automated Critic Feedback & Scoring</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    Research Mind · Autonomous Multi-Agent Pipeline · Streamlit Deployment
</div>
""", unsafe_allow_html=True)