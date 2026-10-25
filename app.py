"""Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1 • Production-Ready Streamlit Application.
Autonomous Multimodal Civil & Safety Engineering AI.
"""

import streamlit as st
import os

# -------------------------------------------------------------
# 1. Page Configuration (Must be first Streamlit command)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. Inject Custom Responsive CSS Design System
# -------------------------------------------------------------
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import module components
from modules.config import APP_TITLE, APP_SUBTITLE, VERSION, STANDARDS
from modules.ppe_audit import render_ppe_audit_tab
from modules.structural_diagnostics import render_crack_diagnostics_tab
from modules.planning_valuation import render_planning_valuation_tab
from modules.site_assistant import render_site_assistant_tab


# -------------------------------------------------------------
# 3. Sidebar: Configuration, API Keys, Architecture & Telemetry
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
        <span style="font-size: 2rem;">🏗️</span>
        <div>
            <div style="font-size: 1.1rem; font-weight: 800; color: #ffffff; line-height: 1.2;">
                CONSTRUCT-AI
            </div>
            <div style="font-size: 0.72rem; color: #f59e0b; font-weight: 700; letter-spacing: 0.5px;">
                CAPSTONE PROJECT 1
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔑 Google Gemini Vision API")
    
    # Read environment variable if pre-configured
    default_env_key = os.environ.get("GEMINI_API_KEY", "")

    api_key_input = st.text_input(
        "Enter Gemini API Key:",
        value=default_env_key,
        type="password",
        placeholder="AIzaSy...",
        help="Supply your Google AI Studio API key for live multimodal vision inference. If omitted, platform seamlessly runs in high-fidelity Demonstration Mode."
    )

    model_name = st.selectbox(
        "⚡ Gemini Vision Model:",
        options=[
            "gemini-2.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash",
            "gemini-1.5-flash"
        ],
        index=0,
        help="Select foundation multimodal vision model for structural pathology & PPE audits."
    )

    force_demo = st.checkbox(
        "Force Demonstration Mode",
        value=False,
        help="Force deterministic offline AI simulation without expending Gemini API tokens."
    )

    # Live Mode Status Pill
    if force_demo:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 10px; margin: 10px 0;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #fbbf24;">⚡ DEMONSTRATION MODE ACTIVE</div>
            <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 2px;">Using verified offline synthetic models & deterministic benchmarks.</div>
        </div>
        """, unsafe_allow_html=True)
    elif api_key_input and api_key_input.strip():
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px; margin: 10px 0;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #34d399;">🟢 LIVE MULTIMODAL GEMINI ACTIVE</div>
            <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 2px;">Connected to Google Gemini API for real-time vision inference.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); border-radius: 8px; padding: 10px; margin: 10px 0;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #60a5fa;">ℹ️ ZERO-KEY DEMO MODE</div>
            <div style="font-size: 0.75rem; color: #cbd5e1; margin-top: 2px;">No API key detected. Running interactive demonstration mode with built-in benchmarks.</div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Architecture Overview Expander
    # -------------------------------------------------------------
    st.markdown("---")
    with st.expander("🏛️ System Architecture & Framework", expanded=False):
        st.markdown("""
        **Multi-Tier Autonomous Civil AI Stack:**
        1. **Multimodal Ingestion**: High-res field photo capture (scaffolding, concrete surfaces, excavation).
        2. **Foundation AI**: Google Gemini Multimodal Vision API (`gemini-2.5-flash`).
        3. **Regulatory Logic Engines**:
           - **OSHA 1926**: Fall protection & PPE compliance rules.
           - **IS 456:2000**: Concrete crack limits (<0.3mm) & deshuttering periods.
           - **NBC 2016 Part 7**: Site management & weather safety protocols.
        4. **Generative Synthesis**: Pollinations AI 3D architectural rendering & multi-turn engineering conversational copilot.
        5. **Edge Delivery**: Responsive Streamlit Cloud zero-database architecture.
        """)

    # Standards Badges in Sidebar
    with st.expander("📜 Governed Engineering Standards", expanded=False):
        for std_key, std_name in STANDARDS.items():
            st.markdown(f"- **{std_key}**: {std_name}")

    # App Metadata Footer
    st.markdown("---")
    st.caption(f"Platform: **v{VERSION}** • Skill Wallet Capstone 1")
    if st.button("🔄 Reset Platform State", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# -------------------------------------------------------------
# 4. Main Page Header Banner
# -------------------------------------------------------------
st.markdown(f"""
<div class="brand-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <h1>
            <span>🏗️</span> {APP_TITLE}
        </h1>
        <span class="brand-badge">Skill Wallet Capstone Project 1</span>
    </div>
    <p class="brand-sub">{APP_SUBTITLE}</p>
    <div class="standards-row">
        <span class="pill-standard">OSHA 1926 Subpart E & M</span>
        <span class="pill-standard">IS 456:2000 (Concrete Code)</span>
        <span class="pill-standard">IS 2925 (Industrial Helmets)</span>
        <span class="pill-standard">IS 15809 (High-Vis Vests)</span>
        <span class="pill-standard">ACI 224R-01 (Crack Control)</span>
        <span class="pill-standard">NBC 2016 (National Building Code)</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# 5. Core Navigation Tabs
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Tab 1: Site Safety & PPE Audit (Epic 2)",
    "🔍 Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)",
    "📐 Tab 3: Planning & Real Estate Valuation (Epic 3)",
    "🌦️ Tab 4: Daily Site Assistant & Weather Advisory (Epic 5)"
])

with tab1:
    render_ppe_audit_tab(api_key=api_key_input, model_name=model_name, force_demo=force_demo)

with tab2:
    render_crack_diagnostics_tab(api_key=api_key_input, model_name=model_name, force_demo=force_demo)

with tab3:
    render_planning_valuation_tab()

with tab4:
    render_site_assistant_tab(api_key=api_key_input, model_name=model_name, force_demo=force_demo)


# -------------------------------------------------------------
# 6. Global Platform Footer
# -------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 12px 0 20px 0;">
    <strong>Multimodal Construction Intelligence Platform</strong> • Skill Wallet Capstone Project 1<br/>
    Engineered for zero-database 1-click deployment on Streamlit Community Cloud • Compliant with OSHA 1926 & IS 456:2000.
</div>
""", unsafe_allow_html=True)
