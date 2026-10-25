"""Tab 1: Site Safety & PPE Audit Module (Epic 2).
AI-driven computer vision safety compliance checking under OSHA 1926 & IS 456 / IS 2925.
"""

import streamlit as st
import json
from PIL import Image
import io
from modules.sample_data import (
    SAMPLE_PPE_PHOTOS,
    create_synthetic_image,
    get_image_bytes
)
from modules.gemini_client import analyze_ppe_multimodal


def render_ppe_audit_tab(api_key: str, model_name: str, force_demo: bool):
    """Render the Site Safety & PPE Audit Tab UI and handlers."""
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #ffffff;">
            🛡️ Site Safety & PPE Compliance Audit Engine
        </h2>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.92rem;">
            Multimodal computer vision auditing worker PPE (helmets, high-vis vests, steel-toe boots, fall harnesses) 
            under <strong>OSHA 1926</strong>, <strong>IS 2925</strong>, and <strong>IS 15809</strong> standards.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize state keys if not present
    if "ppe_image_bytes" not in st.session_state:
        st.session_state.ppe_image_bytes = None
    if "ppe_image_pil" not in st.session_state:
        st.session_state.ppe_image_pil = None
    if "ppe_sample_key" not in st.session_state:
        st.session_state.ppe_sample_key = None
    if "ppe_result" not in st.session_state:
        st.session_state.ppe_result = None

    # Two-column layout for Input & Inspection Zone
    col_input, col_preview = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown("#### 📸 1. Select or Upload Site Inspection Photo")
        
        # Sample Presets Selection
        sample_options = ["None (Upload Custom Photo)"] + list(SAMPLE_PPE_PHOTOS.keys())
        selected_sample = st.selectbox(
            "⚡ Quick-Load Inspection Presets:",
            options=sample_options,
            index=1 if st.session_state.ppe_sample_key is None else (
                sample_options.index(st.session_state.ppe_sample_key) 
                if st.session_state.ppe_sample_key in sample_options else 0
            ),
            help="Select a benchmark construction site photo or choose 'Upload Custom Photo'."
        )

        # Handle sample selection
        if selected_sample != "None (Upload Custom Photo)":
            if st.session_state.ppe_sample_key != selected_sample:
                st.session_state.ppe_sample_key = selected_sample
                sample_meta = SAMPLE_PPE_PHOTOS[selected_sample]
                img = create_synthetic_image(sample_meta["title"], sample_meta["subtitle"], sample_meta["theme"])
                st.session_state.ppe_image_pil = img
                st.session_state.ppe_image_bytes = get_image_bytes(img)
                # Auto-populate mock results for instant feedback
                st.session_state.ppe_result = sample_meta["mock_result"]
        else:
            if st.session_state.ppe_sample_key is not None:
                st.session_state.ppe_sample_key = None
                st.session_state.ppe_image_bytes = None
                st.session_state.ppe_image_pil = None
                st.session_state.ppe_result = None

        # Custom File Uploader
        uploaded_file = st.file_uploader(
            "📁 Or Upload Site Image (JPG / PNG):",
            type=["jpg", "jpeg", "png"],
            help="Upload high-resolution field photos of scaffolding, excavations, or rebar staging."
        )

        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            st.session_state.ppe_image_bytes = bytes_data
            st.session_state.ppe_image_pil = Image.open(io.BytesIO(bytes_data))
            st.session_state.ppe_sample_key = None

        # Audit Trigger Action
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        audit_btn = st.button(
            "🔍 Run Multimodal PPE & Safety Audit",
            type="primary",
            use_container_width=True,
            disabled=(st.session_state.ppe_image_bytes is None)
        )

        if audit_btn and st.session_state.ppe_image_bytes is not None:
            with st.spinner("Analyzing site imagery with Gemini Multimodal Safety Vision..."):
                result = analyze_ppe_multimodal(
                    image_bytes=st.session_state.ppe_image_bytes,
                    mime_type="image/png",
                    api_key=api_key,
                    model_name=model_name,
                    sample_key=st.session_state.ppe_sample_key,
                    force_demo=force_demo
                )
                st.session_state.ppe_result = result
                st.success("✅ Multimodal Safety Audit Complete!")

    with col_preview:
        st.markdown("#### 🖼️ Active Site Imagery Preview")
        if st.session_state.ppe_image_pil is not None:
            st.image(st.session_state.ppe_image_pil, use_container_width=True)
            if st.session_state.ppe_sample_key:
                st.info(f"📌 Loaded Preset: **{st.session_state.ppe_sample_key}**")
            else:
                st.caption("Active custom upload undergoing inspection.")
        else:
            st.markdown("""
            <div style="border: 2px dashed rgba(255, 255, 255, 0.15); border-radius: 12px; padding: 40px 20px; text-align: center; color: #64748b;">
                <p style="font-size: 2.5rem; margin: 0 0 10px 0;">🏗️</p>
                <p style="margin: 0; font-size: 0.95rem; font-weight: 500;">No site photo loaded yet.</p>
                <p style="margin: 4px 0 0 0; font-size: 0.8rem;">Select a preset above or upload an inspection photo.</p>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Render Audit Results if Available
    # -------------------------------------------------------------
    if st.session_state.ppe_result:
        res = st.session_state.ppe_result
        st.markdown("---")
        st.markdown("### 📊 Safety Compliance Telemetry & Audit Report")

        # Top Metric Cards Row
        score = res.get("safety_score", 0)
        status = res.get("overall_status", "Audited")
        workers = res.get("workers_detected", 0)
        hazards = res.get("identified_hazards", [])
        engine_label = res.get("_engine", "Multimodal Engine")

        # Color coding logic
        if score >= 85:
            score_color = "#10b981"
            status_badge = f'<span class="badge-compliant">🟢 {status}</span>'
        elif score >= 60:
            score_color = "#f59e0b"
            status_badge = f'<span class="badge-warning">🟡 {status}</span>'
        else:
            score_color = "#ef4444"
            status_badge = f'<span class="badge-critical">🔴 {status}</span>'

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-container" style="border-top: 3px solid {score_color};">
                <div class="metric-title">Safety Score</div>
                <div class="metric-val" style="color: {score_color};">{score}/100</div>
                <div class="metric-desc">OSHA / IS Compliance Index</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Overall Status</div>
                <div style="margin: 8px 0;">{status_badge}</div>
                <div class="metric-desc">Risk Severity Classification</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Personnel Detected</div>
                <div class="metric-val">{workers}</div>
                <div class="metric-desc">Active Zone Crew Count</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Identified Hazards</div>
                <div class="metric-val" style="color: {'#ef4444' if len(hazards) > 0 else '#10b981'};">{len(hazards)}</div>
                <div class="metric-desc">Remediation Action Items</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(f"Engine: **{engine_label}** • Audit Timestamp: {res.get('audit_timestamp', 'Live Verified')}")

        # -------------------------------------------------------------
        # PPE Detection Checklist Table
        # -------------------------------------------------------------
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🦺 PPE Compliance Checklist")

        ppe_items = res.get("ppe_detection", [])
        if ppe_items:
            for item in ppe_items:
                item_name = item.get("item", "PPE Item")
                item_status = item.get("status", "Unknown")
                comp_count = item.get("compliant_count", 0)
                tot_workers = item.get("total_workers", 0)
                std = item.get("standard", "OSHA 1926")
                notes = item.get("notes", "")

                if "Compliant" in item_status and "Non" not in item_status:
                    pill_html = '<span class="badge-compliant">✓ Compliant</span>'
                    border_color = "rgba(16, 185, 129, 0.3)"
                elif "Partial" in item_status:
                    pill_html = '<span class="badge-warning">⚠ Partial</span>'
                    border_color = "rgba(245, 158, 11, 0.3)"
                elif "Not Applicable" in item_status:
                    pill_html = '<span class="badge-info">N/A</span>'
                    border_color = "rgba(100, 116, 139, 0.3)"
                else:
                    pill_html = '<span class="badge-critical">✕ Violation</span>'
                    border_color = "rgba(239, 68, 68, 0.4)"

                st.markdown(f"""
                <div style="background: rgba(22, 28, 42, 0.7); border: 1px solid {border_color}; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 700; color: #ffffff; font-size: 0.96rem;">{item_name}</div>
                        <div style="color: #94a3b8; font-size: 0.82rem; margin-top: 2px;">Standard: <span style="font-family: 'JetBrains Mono', monospace; color: #cbd5e1;">{std}</span> • Detected: {comp_count}/{tot_workers} compliant</div>
                        <div style="color: #e2e8f0; font-size: 0.85rem; margin-top: 4px;">{notes}</div>
                    </div>
                    <div style="margin-left: 16px; flex-shrink: 0;">
                        {pill_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # Identified Hazards & Corrective Remedies
        # -------------------------------------------------------------
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🚨 Identified Site Hazards & Actionable Remedies")

        if hazards:
            for hz in hazards:
                severity = hz.get("severity", "Medium")
                h_title = hz.get("hazard", "Identified Site Risk")
                loc = hz.get("location", "Active Zone")
                citation = hz.get("osha_citation", "OSHA 1926")
                remedy = hz.get("remedy", "Take corrective safety action.")

                sev_class = f"severity-{severity.lower()}"
                if severity == "Critical":
                    sev_badge = '<span class="badge-critical">CRITICAL HAZARD</span>'
                elif severity == "High":
                    sev_badge = '<span class="badge-critical" style="background: rgba(249, 115, 22, 0.2); color: #fb923c; border-color: rgba(249, 115, 22, 0.4);">HIGH RISK</span>'
                elif severity == "Medium":
                    sev_badge = '<span class="badge-warning">MEDIUM RISK</span>'
                else:
                    sev_badge = '<span class="badge-info">LOW RISK</span>'

                st.markdown(f"""
                <div class="hazard-card {sev_class}">
                    <div class="hazard-header">
                        <span class="hazard-title">{h_title}</span>
                        <div>{sev_badge}</div>
                    </div>
                    <div style="display: flex; gap: 10px; margin-bottom: 6px;">
                        <span class="hazard-citation">📍 {loc}</span>
                        <span class="hazard-citation">📜 {citation}</span>
                    </div>
                    <div class="hazard-remedy">
                        <strong>🛠️ Corrective Engineering Remedy:</strong><br/>
                        {remedy}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("🎉 No high-risk safety hazards identified in this site capture!")

        # -------------------------------------------------------------
        # Priority Recommendations Summary
        # -------------------------------------------------------------
        recs = res.get("recommendations_summary", [])
        if recs:
            st.markdown("#### 📋 Priority Safety Recommendations")
            for r in recs:
                st.markdown(f"- {r}")

        # -------------------------------------------------------------
        # Downloadable Reports
        # -------------------------------------------------------------
        st.markdown("---")
        dcol1, dcol2 = st.columns(2)
        
        with dcol1:
            json_str = json.dumps(res, indent=2)
            st.download_button(
                label="📥 Download Structured JSON Report",
                data=json_str,
                file_name="site_safety_ppe_audit.json",
                mime="application/json",
                use_container_width=True
            )

        with dcol2:
            # Generate Executive Safety Certificate Text
            cert_lines = [
                "=" * 60,
                "MULTIMODAL CONSTRUCTION INTELLIGENCE PLATFORM",
                "SITE SAFETY & PPE COMPLIANCE AUDIT CERTIFICATE",
                "=" * 60,
                f"Timestamp: {res.get('audit_timestamp', 'Live Verified')}",
                f"Overall Safety Score: {score}/100",
                f"Compliance Status: {status}",
                f"Workers Audited: {workers}",
                f"Regulatory Standards: OSHA 1926, IS 456, IS 2925, IS 15809",
                "-" * 60,
                "IDENTIFIED HAZARDS & ACTIONABLE REMEDIES:"
            ]
            for i, h in enumerate(hazards, 1):
                cert_lines.append(f"{i}. [{h.get('severity')}] {h.get('hazard')} (Loc: {h.get('location')})")
                cert_lines.append(f"   Citation: {h.get('osha_citation')}")
                cert_lines.append(f"   Action: {h.get('remedy')}")
            cert_lines.append("-" * 60)
            cert_lines.append("RECOMMENDATIONS:")
            for r in recs:
                cert_lines.append(f"• {r}")
            cert_lines.append("=" * 60)
            cert_text = "\n".join(cert_lines)

            st.download_button(
                label="📄 Download Safety Audit Certificate (TXT)",
                data=cert_text,
                file_name="safety_audit_certificate.txt",
                mime="text/plain",
                use_container_width=True
            )
