"""Tab 3: Planning & Real Estate Valuation Module (Epic 3).
Techno-economic CapEx forecasting, civil material takeoff, milestone progress tracking,
and Pollinations AI 3D architectural concept visualization.
"""

import streamlit as st
import urllib.parse
import random
from modules.config import (
    COST_BENCHMARKS,
    LOCATION_TIERS,
    CONSTRUCTION_MILESTONES
)


def format_inr(amount_inr: float) -> str:
    """Format numerical INR currency into Crores (Cr) or Lakhs (L)."""
    if amount_inr >= 10_000_000:
        crores = amount_inr / 10_000_000
        return f"₹{crores:,.2f} Cr"
    elif amount_inr >= 100_000:
        lakhs = amount_inr / 100_000
        return f"₹{lakhs:,.2f} L"
    else:
        return f"₹{amount_inr:,.0f}"


def render_planning_valuation_tab():
    """Render the Planning & Real Estate Valuation Tab UI and handlers."""
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #ffffff;">
            📐 Construction CapEx Planning & Asset Valuation Engine
        </h2>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.92rem;">
            Techno-economic project cost modeling, civil material requirement takeoff (Steel/Cement/RMC),
            stage-wise milestone tracking, and generative <strong>Pollinations AI 3D architectural rendering</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Interactive Controls Panel
    # -------------------------------------------------------------
    with st.container():
        st.markdown("#### ⚙️ 1. Project Parameters & Site Geometry")
        pcol1, pcol2, pcol3, pcol4 = st.columns([1.2, 1, 1.2, 1])

        with pcol1:
            structure_types = list(COST_BENCHMARKS.keys())
            structure_type = st.selectbox(
                "🏗️ Structure Type:",
                options=structure_types,
                index=0,
                help="Type of civil asset determining structural member sizes and material densities."
            )

        with pcol2:
            built_up_sqft = st.number_input(
                "📏 Built-up Area (Sq. Ft.):",
                min_value=1000,
                max_value=2000000,
                value=50000,
                step=5000,
                help="Gross built-up area (BUA) in square feet including common circulation areas."
            )

        with pcol3:
            location_tiers = list(LOCATION_TIERS.keys())
            selected_tier = st.selectbox(
                "📍 Location Tier (Indian Cities):",
                options=location_tiers,
                index=0,
                help="Tier 1 has higher land valuation and labor multipliers."
            )

        with pcol4:
            spec_grade = st.selectbox(
                "✨ Specification Grade:",
                options=["Standard", "Premium", "Ultra-Luxury"],
                index=1,
                help="Finishing specifications and structural grade."
            )

        # Completion Percentage Slider
        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
        completion_pct = st.slider(
            "⏳ Project Completion Milestone (%):",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            format="%d%%",
            help="Current construction progress across foundation, superstructure, MEP, and finishes."
        )

    # -------------------------------------------------------------
    # Techno-Economic Calculations
    # -------------------------------------------------------------
    tier_info = LOCATION_TIERS[selected_tier]
    tier_multiplier = tier_info["multiplier"]
    market_multiplier = tier_info["market_val_multiplier"]

    benchmark_data = COST_BENCHMARKS[structure_type]
    base_rate_sqft = benchmark_data[spec_grade] * tier_multiplier
    
    total_project_budget = built_up_sqft * base_rate_sqft
    capex_incurred = total_project_budget * (completion_pct / 100.0)
    capex_remaining = total_project_budget - capex_incurred

    # Asset Valuation dynamics:
    # At 0%, asset valuation = land basis (~60% of total capex * market multiplier).
    # As completion advances, market realization discount shrinks and finished asset premium unlocks.
    completion_alpha = (completion_pct / 100.0)
    risk_discount = 0.85 + (0.15 * completion_alpha)
    current_asset_valuation = (
        total_project_budget * market_multiplier * (0.60 + 0.40 * completion_alpha) * risk_discount
    )

    # Material Quantity Takeoffs
    steel_kg_sqft = benchmark_data["steel_per_sqft_kg"]
    cement_bags_sqft = benchmark_data["cement_per_sqft_bags"]
    
    total_steel_kg = built_up_sqft * steel_kg_sqft
    total_steel_mt = total_steel_kg / 1000.0 # Metric Tonnes
    steel_consumed_mt = total_steel_mt * (completion_pct / 100.0)

    total_cement_bags = int(built_up_sqft * cement_bags_sqft)
    cement_consumed_bags = int(total_cement_bags * (completion_pct / 100.0))
    total_rmc_m3 = (total_cement_bags * 50) / 360 # approx 360kg cement per m3 M30 concrete

    # -------------------------------------------------------------
    # Financial Telemetry & Valuation Metrics
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 💰 Financial Telemetry & Valuation Metrics")

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #3b82f6;">
            <div class="metric-title">Total Project Budget</div>
            <div class="metric-val" style="color: #60a5fa;">{format_inr(total_project_budget)}</div>
            <div class="metric-desc">@ ₹{base_rate_sqft:,.0f} / sq.ft.</div>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #f59e0b;">
            <div class="metric-title">CapEx Incurred to Date</div>
            <div class="metric-val" style="color: #fbbf24;">{format_inr(capex_incurred)}</div>
            <div class="metric-desc">{completion_pct}% completion expended</div>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #ef4444;">
            <div class="metric-title">Remaining CapEx</div>
            <div class="metric-val" style="color: #f87171;">{format_inr(capex_remaining)}</div>
            <div class="metric-desc">{100 - completion_pct}% balance to fund</div>
        </div>
        """, unsafe_allow_html=True)

    with f4:
        st.markdown(f"""
        <div class="metric-container" style="border-top: 3px solid #10b981;">
            <div class="metric-title">Current Asset Valuation</div>
            <div class="metric-val" style="color: #34d399;">{format_inr(current_asset_valuation)}</div>
            <div class="metric-desc">Market equity value today</div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Milestone Stage Breakdown
    # -------------------------------------------------------------
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🚩 Milestone Progress & Phase Status")

    # Determine current active phase
    active_phase_name = "Commissioning & Handover"
    for phase in CONSTRUCTION_MILESTONES:
        start_p, end_p = phase["range"]
        if start_p <= completion_pct <= end_p:
            active_phase_name = phase["name"]
            break

    st.progress(completion_pct / 100.0)
    st.caption(f"Currently Active Stage: **{active_phase_name}** ({completion_pct}% Overall Physical Progress)")

    # Milestone Grid
    m_cols = st.columns(len(CONSTRUCTION_MILESTONES))
    for i, phase in enumerate(CONSTRUCTION_MILESTONES):
        start_p, end_p = phase["range"]
        with m_cols[i]:
            if completion_pct >= end_p:
                pill = '<span class="badge-compliant" style="font-size: 0.72rem;">✓ Completed</span>'
                card_border = "rgba(16, 185, 129, 0.4)"
            elif start_p <= completion_pct < end_p:
                pill = '<span class="badge-warning" style="font-size: 0.72rem;">⚡ In Progress</span>'
                card_border = "rgba(245, 158, 11, 0.5)"
            else:
                pill = '<span class="badge-info" style="font-size: 0.72rem;">⏳ Upcoming</span>'
                card_border = "rgba(100, 116, 139, 0.25)"

            st.markdown(f"""
            <div style="background: rgba(22, 28, 42, 0.75); border: 1px solid {card_border}; border-radius: 8px; padding: 10px; min-height: 125px;">
                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">Phase {i+1} ({start_p}-{end_p}%)</div>
                <div style="font-size: 0.82rem; font-weight: 700; color: #ffffff; margin: 4px 0;">{phase['name']}</div>
                <div style="margin: 4px 0;">{pill}</div>
                <div style="font-size: 0.72rem; color: #cbd5e1; line-height: 1.25;">{phase['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Civil Material Requirement Metrics
    # -------------------------------------------------------------
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🧱 Civil Structural Material Takeoff (Indian Benchmarks)")

    mat1, mat2, mat3, mat4 = st.columns(4)
    with mat1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Fe500D TMT Steel</div>
            <div class="metric-val">{total_steel_mt:,.1f} MT</div>
            <div class="metric-desc">Consumed: {steel_consumed_mt:,.1f} MT ({completion_pct}%)</div>
        </div>
        """, unsafe_allow_html=True)

    with mat2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">OPC 53 / PPC Cement</div>
            <div class="metric-val">{total_cement_bags:,.0f} Bags</div>
            <div class="metric-desc">Consumed: {cement_consumed_bags:,.0f} Bags (50kg)</div>
        </div>
        """, unsafe_allow_html=True)

    with mat3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Ready-Mix Concrete</div>
            <div class="metric-val">{total_rmc_m3:,.0f} m³</div>
            <div class="metric-desc">M25 - M40 Grade Concrete</div>
        </div>
        """, unsafe_allow_html=True)

    with mat4:
        sand_cft = built_up_sqft * benchmark_data["sand_per_sqft_cft"]
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">Manufactured Sand</div>
            <div class="metric-val">{sand_cft / 100:,.1f} Brass</div>
            <div class="metric-desc">{sand_cft:,.0f} CFT M-Sand Volume</div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Conceptual 3D Architectural Rendering via Pollinations AI
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🏛️ Conceptual 3D Architectural Rendering (Pollinations AI Integration)")
    st.markdown("""
    Generate state-of-the-art conceptual architectural visual models directly from your site geometry, 
    structural typology, and aesthetic design specifications.
    """)

    # Seed and prompt management
    if "render_seed" not in st.session_state:
        st.session_state.render_seed = random.randint(1000, 99999)
    if "render_prompt" not in st.session_state:
        st.session_state.render_prompt = ""

    r_col1, r_col2 = st.columns([1, 1], gap="medium")

    with r_col1:
        st.markdown("##### 🎨 Architectural Design Parameters")
        arch_style = st.selectbox(
            "Architectural Facade Style:",
            options=[
                "Biophilic Sustainable High-Tech with cantilevered sky gardens",
                "Ultra-Modern Sleek Glazed Curtain Wall with titanium bronze mullions",
                "Post-Modern Brutalist Textured Concrete with recessed geometric fenestrations",
                "Contemporary Neo-Classical Luxury with double-height colonnades",
                "Parametric Aerodynamic Steel & Glass Organic Structure"
            ],
            index=0
        )

        lighting_atmosphere = st.selectbox(
            "Lighting & Environmental Atmosphere:",
            options=[
                "Crisp golden hour twilight architectural photography with warm interior glows",
                "Direct bright midday sun showcasing structural shadow definition",
                "Dusk blue hour drone aerial elevation with urban skyline reflection",
                "Cinematic overcast mist with soft diffused atmospheric shadows"
            ],
            index=0
        )

        # Dynamic default prompt synthesis
        default_prompt = (
            f"Hyper-realistic 8k architectural photograph of a {spec_grade.lower()} {structure_type.lower()}, "
            f"{built_up_sqft:,} sq ft gross area, {arch_style}, {lighting_atmosphere}, "
            f"photographed with Hasselblad H6D-100c, tilt-shift architectural lens, highly detailed textures, "
            f"professional architectural rendering, Unreal Engine 5 aesthetic, photorealistic masterpiece."
        )

        custom_prompt = st.text_area(
            "📝 Generative 3D Architectural Prompt (Customizable):",
            value=default_prompt,
            height=130,
            help="Fine-tune your visual concept instructions before rendering."
        )

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            gen_btn = st.button("✨ Generate 3D Concept Render", type="primary", use_container_width=True)
        with b_c2:
            seed_btn = st.button("🎲 Randomize Aesthetic Seed", use_container_width=True)

        if seed_btn:
            st.session_state.render_seed = random.randint(1000, 99999)
            st.rerun()

        if gen_btn:
            st.session_state.render_prompt = custom_prompt
            st.session_state.render_seed = random.randint(1000, 99999)

    # Encode prompt for Pollinations AI
    active_prompt = st.session_state.render_prompt if st.session_state.render_prompt else default_prompt
    encoded_prompt = urllib.parse.quote(active_prompt)
    pollinations_url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width=1024&height=640&seed={st.session_state.render_seed}&nologo=true"
    )

    with r_col2:
        st.markdown("##### 🖼️ Generative 3D Visual Preview")
        st.image(
            pollinations_url,
            caption=f"AI Concept: {structure_type} ({spec_grade}) • Seed #{st.session_state.render_seed}",
            use_container_width=True
        )
        st.caption("Rendered live via Pollinations AI Neural Synthesis API.")
        st.markdown(f"[🔗 Open Full-Resolution 1024x640 Render]({pollinations_url})")
