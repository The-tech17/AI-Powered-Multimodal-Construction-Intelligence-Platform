"""Tab 2: Crack Diagnostics & Structural Integrity Module (Epic 2).
Multimodal classification of concrete defect types under IS 456:2000 & ACI 224R-01.
"""

import streamlit as st
import json
from PIL import Image
import io
from modules.sample_data import (
    SAMPLE_CRACK_PHOTOS,
    create_synthetic_image,
    get_image_bytes
)
from modules.gemini_client import analyze_crack_multimodal


def render_crack_diagnostics_tab(api_key: str, model_name: str, force_demo: bool):
    """Render the Crack Diagnostics & Structural Integrity Tab UI and handlers."""
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #ffffff;">
            🔍 Crack Diagnostics & Structural Integrity Engine
        </h2>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.92rem;">
            Multimodal computer vision classifying concrete surface pathologies (<strong>Shear, Settlement, Spalling, Hairline, Thermal</strong>),
            estimating crack width (mm), and prescribing engineering repairs under <strong>IS 456:2000 Clause 35.3.2</strong> & <strong>ACI 224R-01</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # State initialization
    if "crack_image_bytes" not in st.session_state:
        st.session_state.crack_image_bytes = None
    if "crack_image_pil" not in st.session_state:
        st.session_state.crack_image_pil = None
    if "crack_sample_key" not in st.session_state:
        st.session_state.crack_sample_key = None
    if "crack_result" not in st.session_state:
        st.session_state.crack_result = None

    col_input, col_preview = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("#### 🧱 1. Select or Upload Concrete Surface Photo")

        crack_sample_options = ["None (Upload Custom Defect Photo)"] + list(SAMPLE_CRACK_PHOTOS.keys())
        selected_sample = st.selectbox(
            "⚡ Quick-Load Concrete Defect Presets:",
            options=crack_sample_options,
            index=1 if st.session_state.crack_sample_key is None else (
                crack_sample_options.index(st.session_state.crack_sample_key) 
                if st.session_state.crack_sample_key in crack_sample_options else 0
            ),
            help="Select a benchmark structural crack pattern or upload a field photo."
        )

        if selected_sample != "None (Upload Custom Defect Photo)":
            if st.session_state.crack_sample_key != selected_sample:
                st.session_state.crack_sample_key = selected_sample
                sample_meta = SAMPLE_CRACK_PHOTOS[selected_sample]
                img = create_synthetic_image(sample_meta["title"], sample_meta["subtitle"], sample_meta["theme"])
                st.session_state.crack_image_pil = img
                st.session_state.crack_image_bytes = get_image_bytes(img)
                st.session_state.crack_result = sample_meta["mock_result"]
        else:
            if st.session_state.crack_sample_key is not None:
                st.session_state.crack_sample_key = None
                st.session_state.crack_image_bytes = None
                st.session_state.crack_image_pil = None
                st.session_state.crack_result = None

        uploaded_file = st.file_uploader(
            "📁 Or Upload Concrete Surface Photo (JPG / PNG):",
            type=["jpg", "jpeg", "png"],
            help="Upload high-res photos of beams, slabs, columns, masonry infill, or foundation walls."
        )

        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            st.session_state.crack_image_bytes = bytes_data
            st.session_state.crack_image_pil = Image.open(io.BytesIO(bytes_data))
            st.session_state.crack_sample_key = None

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        diag_btn = st.button(
            "🔬 Run Forensic Crack & Defect Diagnostic",
            type="primary",
            use_container_width=True,
            disabled=(st.session_state.crack_image_bytes is None)
        )

        if diag_btn and st.session_state.crack_image_bytes is not None:
            with st.spinner("Analyzing concrete morphology & pathology with Gemini Structural AI..."):
                result = analyze_crack_multimodal(
                    image_bytes=st.session_state.crack_image_bytes,
                    mime_type="image/png",
                    api_key=api_key,
                    model_name=model_name,
                    sample_key=st.session_state.crack_sample_key,
                    force_demo=force_demo
                )
                st.session_state.crack_result = result
                st.success("✅ Forensic Diagnostic Complete!")

    with col_preview:
        st.markdown("#### 🔬 Structural Surface Inspection Viewport")
        if st.session_state.crack_image_pil is not None:
            st.image(st.session_state.crack_image_pil, use_container_width=True)
            if st.session_state.crack_sample_key:
                st.info(f"📌 Diagnostic Pattern: **{st.session_state.crack_sample_key}**")
            else:
                st.caption("Active uploaded concrete surface under diagnostic analysis.")
        else:
            st.markdown("""
            <div style="border: 2px dashed rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 40px 20px; text-align: center; color: #64748b;">
                <p style="font-size: 2.5rem; margin: 0 0 10px 0;">🧱</p>
                <p style="margin: 0; font-size: 0.95rem; font-weight: 500;">No concrete photo loaded.</p>
                <p style="margin: 4px 0 0 0; font-size: 0.8rem;">Select a defect preset or upload a structural member image.</p>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Diagnostic Telemetry & Engineering Prescription
    # -------------------------------------------------------------
    if st.session_state.crack_result:
        res = st.session_state.crack_result
        st.markdown("---")
        st.markdown("### 📋 Forensic Structural Assessment & Engineering Prescription")

        defect_type = res.get("defect_type", "Structural Crack")
        subtype = res.get("subtype", "Concrete Fissure")
        width_mm = res.get("crack_width_mm", 0.0)
        urgency = res.get("urgency", "Moderate Monitoring & Repair")
        risk_score = res.get("risk_score", 50)
        is_exceeded = res.get("is_456_limit_exceeded", width_mm > 0.3)
        clause_ref = res.get("is_456_clause", "IS 456:2000 Clause 35.3.2")
        engine_label = res.get("_engine", "Multimodal Structural Vision")

        # Urgency badges
        if "Immediate" in urgency or "Urgent" in urgency:
            urgency_badge = f'<span class="badge-critical">⚠️ {urgency}</span>'
            risk_color = "#ef4444"
        elif "Moderate" in urgency:
            urgency_badge = f'<span class="badge-warning">⚡ {urgency}</span>'
            risk_color = "#f59e0b"
        else:
            urgency_badge = f'<span class="badge-compliant">✓ {urgency}</span>'
            risk_color = "#10b981"

        # Metric Cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-container" style="border-top: 3px solid #3b82f6;">
                <div class="metric-title">Defect Classification</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #ffffff; margin-top: 4px;">{defect_type}</div>
                <div class="metric-desc">{subtype}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            width_color = "#ef4444" if is_exceeded else "#10b981"
            st.markdown(f"""
            <div class="metric-container" style="border-top: 3px solid {width_color};">
                <div class="metric-title">Est. Crack Width</div>
                <div class="metric-val" style="color: {width_color};">{width_mm:.2f} mm</div>
                <div class="metric-desc">Limit: 0.30 mm ({'Exceeded ⚠️' if is_exceeded else 'Compliant ✓'})</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-container" style="border-top: 3px solid {risk_color};">
                <div class="metric-title">Structural Risk Index</div>
                <div class="metric-val" style="color: {risk_color};">{risk_score}/100</div>
                <div class="metric-desc">Member Severity Index</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Intervention Urgency</div>
                <div style="margin: 8px 0;">{urgency_badge}</div>
                <div class="metric-desc">Remedial Action Timeline</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(f"Engine: **{engine_label}** • Standard Clause: **{clause_ref}**")

        # Alert if IS 456 Permissible Limit is Exceeded
        if is_exceeded:
            st.warning(f"""
            ⚠️ **IS 456:2000 Clause 35.3.2 Warning**: The observed crack width (**{width_mm:.2f} mm**) exceeds the permissible 
            crack width limit of **0.3 mm** for moderate environmental exposure (**0.2 mm** for severe/marine exposure).
            Active moisture/carbonation ingress will accelerate rebar depassivation. Structural intervention required.
            """)
        else:
            st.success(f"""
            ✓ **IS 456:2000 Compliant**: Crack width of **{width_mm:.2f} mm** is within the nominal 0.3 mm limit.
            Defect is primarily non-structural / aesthetic, requiring superficial sealing without structural shoring.
            """)

        # -------------------------------------------------------------
        # Root Cause Analysis
        # -------------------------------------------------------------
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🔬 Root Cause Forensic Analysis")
        root_causes = res.get("root_causes", [])
        if root_causes:
            for rc in root_causes:
                st.markdown(f"- **Mechanics**: {rc}")

        # -------------------------------------------------------------
        # Recommended Engineering Repairs (Step-by-Step)
        # -------------------------------------------------------------
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🛠️ Recommended Engineering Rehabilitation Sequence")

        repairs = res.get("engineering_repairs", [])
        if repairs:
            for item in repairs:
                st_num = item.get("step", 1)
                st_action = item.get("action", "Repair Step")
                st_det = item.get("details", "")

                st.markdown(f"""
                <div class="repair-step-card">
                    <div class="step-number">{st_num}</div>
                    <div class="step-content">
                        <div class="step-action">{st_action}</div>
                        <div class="step-details">{st_det}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Material Specification and Monitoring Protocols
        mat_col, mon_col = st.columns(2)
        with mat_col:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-weight: 700; color: #38bdf8; font-size: 0.9rem; margin-bottom: 6px;">🧪 Specified Repair Materials</div>
                <div style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.4;">{res.get('repair_materials', 'Low-viscosity structural epoxy, CFRP wrap, SBR bonding agent.')}</div>
            </div>
            """, unsafe_allow_html=True)

        with mon_col:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 14px;">
                <div style="font-weight: 700; color: #f59e0b; font-size: 0.9rem; margin-bottom: 6px;">📡 Post-Repair Monitoring Protocol</div>
                <div style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.4;">{res.get('monitoring_protocol', 'Periodic ultrasonic pulse velocity (UPV) and Tell-Tale displacement gauge logging.')}</div>
            </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # Downloadable Reports
        # -------------------------------------------------------------
        st.markdown("---")
        dcol1, dcol2 = st.columns(2)

        with dcol1:
            json_str = json.dumps(res, indent=2)
            st.download_button(
                label="📥 Download Diagnostic JSON Data",
                data=json_str,
                file_name="structural_crack_diagnostic.json",
                mime="application/json",
                use_container_width=True
            )

        with dcol2:
            summary_lines = [
                "=" * 60,
                "FORENSIC STRUCTURAL INTEGRITY & DEFECT REPORT",
                "=" * 60,
                f"Classification: {defect_type} ({subtype})",
                f"Estimated Crack Width: {width_mm:.2f} mm",
                f"IS 456 Permissible Limit Exceeded: {'YES' if is_exceeded else 'NO'}",
                f"Reference Standard: {clause_ref}",
                f"Urgency Level: {urgency}",
                f"Structural Risk Score: {risk_score}/100",
                "-" * 60,
                "ENGINEERING ROOT CAUSES:"
            ]
            for c in root_causes:
                summary_lines.append(f"• {c}")
            summary_lines.append("-" * 60)
            summary_lines.append("ENGINEERING REHABILITATION STEPS:")
            for s in repairs:
                summary_lines.append(f"Step {s.get('step')}: {s.get('action')}")
                summary_lines.append(f"  {s.get('details')}")
            summary_lines.append("=" * 60)
            summary_text = "\n".join(summary_lines)

            st.download_button(
                label="📄 Download Forensic Engineering Report (TXT)",
                data=summary_text,
                file_name="structural_defect_report.txt",
                mime="text/plain",
                use_container_width=True
            )
