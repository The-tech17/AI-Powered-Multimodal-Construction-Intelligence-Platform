"""Tab 4: Daily Site Assistant & Weather-Aware Advisory Module (Epic 5).
Dynamic meteorological safety protocols and interactive multi-turn civil engineering copilot.
"""

import streamlit as st
from modules.gemini_client import chat_with_engineering_assistant

# Weather Protocols Knowledge Matrix
WEATHER_PROTOCOLS = {
    "Normal / Favorable (24°C - 32°C, Calm Breeze)": {
        "badge": '<span class="badge-compliant">NORMAL WORKING CONDITIONS</span>',
        "crane_status": "🟢 All tower cranes, mobile hoists, and aerial platforms authorized for full-load operations.",
        "concrete_protocol": "Standard moist curing protocol per IS 456 Clause 13.5 (minimum 7 days continuous hydration for OPC, 10 days for PPC).",
        "electrical_safety": "Routine residual current device (RCD) trip tests; maintain dry conduit inspections.",
        "heights_safety": "Full fall arrest compliance required on perimeters >1.8m per OSHA 1926 Subpart M.",
        "worker_welfare": "Standard 45-minute lunch break with continuous clean potable drinking water access."
    },
    "High Wind & Gale Gusts (>45 km/h / 28 mph)": {
        "badge": '<span class="badge-critical">HIGH WIND ALERT - CRANE RESTRICTION</span>',
        "crane_status": "🔴 MANDATORY CRANE CEASE-WORK: Suspend tower crane slewing and tandem lifts immediately per OSHA 1926.1431. Weather-vane all jib booms in free rotation.",
        "concrete_protocol": "Accelerated surface wind evaporation alert. Apply aliphatic alcohol evaporation retarders and immediate polythene sheeting to stop plastic shrinkage cracking.",
        "electrical_safety": "Inspect overhead temporary electrical lines for sway clearance from metallic scaffolding.",
        "heights_safety": "🔴 STOP WORK on exterior suspended scaffolding and swinging stages above 10 meters. Secure all loose ply sheets, corrugated decking, and formwork props.",
        "worker_welfare": "Require eye protection (sealed goggles) to eliminate windblown aggregate and cement dust corneal abrasion."
    },
    "Heavy Monsoon Rain & Waterlogging": {
        "badge": '<span class="badge-critical">HEAVY MONSOON - ELECTRICAL & FLOOD ALERT</span>',
        "crane_status": "🟡 Ground bearing check required for mobile crane outriggers. Do not operate near saturated unreinforced slopes or excavation lips.",
        "concrete_protocol": "🔴 HALT ALL EXTERIOR CONCRETE SLAB POURS. Rainwater ingress destroys water-cement ratio and washes out cement paste matrix. Protect fresh pours with impermeable tarpaulins.",
        "electrical_safety": "🔴 MANDATORY ELECTRICAL ISOLATION: De-energize all temporary distribution boards (DBs) located in low-lying zones. Ensure IP65 waterproof enclosures and 30mA ELCB breakers.",
        "heights_safety": "Slip-and-fall alert: Steel beam climbing and wet scaffolding decks strictly prohibited. Pump water out of basement access trenches.",
        "worker_welfare": "Deploy sump pumps for deep excavation dewatering per IS 3764. Continuous trench bank stability monitoring for slope liquefaction."
    },
    "Extreme Heat Wave (>42°C / 108°F)": {
        "badge": '<span class="badge-warning">EXTREME HEAT STRESS - HOT WEATHER PROTOCOL</span>',
        "crane_status": "🟡 Monitor hydraulic fluid temperatures on heavy plant and mobile cranes. Check tire pressure spikes.",
        "concrete_protocol": "🔴 HOT WEATHER CONCRETING PROTOCOL (ACI 305R & IS 7861 Part 1): Limit fresh concrete placement temp to <32°C. Use chilled batching water or flaked ice. Continuous wet burlap curing every 90 minutes.",
        "electrical_safety": "Prevent transformer and cable overheating from thermal derating.",
        "heights_safety": "Avoid contact with unshaded structural steel members (surface temperatures can exceed 65°C, causing contact burns).",
        "worker_welfare": "🔴 OSHA HEAT STRESS MANDATE: 15-minute mandatory shade rest every 45 minutes of heavy manual labor. Provide ORS (Oral Rehydration Solution) hydration stations."
    },
    "Severe Thunderstorm & Lightning Warning": {
        "badge": '<span class="badge-critical">LIGHTNING RISK - IMMEDIATE SITE EVACUATION</span>',
        "crane_status": "🔴 30-30 LIGHTNING RULE: Immediate evacuation of all crane operators. Ground tower crane lightning rods to earth pit (<5 ohms resistance).",
        "concrete_protocol": "Cover any active pour areas immediately; postpone batching truck arrivals.",
        "electrical_safety": "Disconnect sensitive surveying telemetry, laser levels, and temporary generators.",
        "heights_safety": "🔴 EVACUATE all roofs, metal scaffolding tiers, rebar fabrication tables, and exposed elevated decks immediately.",
        "worker_welfare": "All personnel must muster inside grounded, permanent site structures. Avoid isolated shipping containers or tree shade."
    },
    "Cold Snap & Freezing Temperatures (<8°C / 46°F)": {
        "badge": '<span class="badge-info">COLD WEATHER - HYDRATION RETARDATION</span>',
        "crane_status": "Warm up hydraulic systems before full-load hoisting. Inspect wire ropes for cold brittleness.",
        "concrete_protocol": "COLD WEATHER CONCRETING (ACI 306R & IS 7861 Part 2): Hydration slows exponentially. Concrete must not freeze before achieving 5 MPa strength. Use heated batching water and insulated curing blankets.",
        "electrical_safety": "Inspect portable space heaters in site offices for fire safety clearance.",
        "heights_safety": "Watch for early morning frost or ice glaze on structural steel beams and metal ladders.",
        "worker_welfare": "Provide warm rest sheds and insulated thermal PPE."
    }
}


def render_site_assistant_tab(api_key: str, model_name: str, force_demo: bool):
    """Render the Daily Site Assistant & Weather-Aware Advisory Tab UI."""
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #ffffff;">
            🌦️ Daily Site Assistant & Weather-Aware Advisory
        </h2>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 0.92rem;">
            Real-time meteorological hazard protocol engine and interactive multi-turn 
            <strong>Civil Engineering Copilot</strong> referencing <strong>IS 456, IS 800, OSHA 1926</strong>, and <strong>NBC 2016</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Weather Advisory Protocol Section
    # -------------------------------------------------------------
    st.markdown("#### 🌤️ 1. Site Environmental Condition & Dynamic Safety Directives")
    weather_options = list(WEATHER_PROTOCOLS.keys())
    
    selected_weather = st.radio(
        "Select Active Meteorological Condition at Construction Site:",
        options=weather_options,
        index=1, # Default to High Wind for dynamic demo impact
        horizontal=True
    )

    proto = WEATHER_PROTOCOLS[selected_weather]

    st.markdown(f"""
    <div class="weather-advisory-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff;">🚨 Active Environmental Safety Protocol</div>
            <div>{proto['badge']}</div>
        </div>
        <div class="protocol-item" style="border-left-color: #ef4444;">
            <strong>🏗️ Crane & Heavy Lifting Directive:</strong><br/>
            {proto['crane_status']}
        </div>
        <div class="protocol-item" style="border-left-color: #f59e0b;">
            <strong>🧪 Concrete Placement & Curing Protocol:</strong><br/>
            {proto['concrete_protocol']}
        </div>
        <div class="protocol-item" style="border-left-color: #06b6d4;">
            <strong>⚡ Electrical & Dewatering Mitigation:</strong><br/>
            {proto['electrical_safety']}
        </div>
        <div class="protocol-item" style="border-left-color: #3b82f6;">
            <strong>🧗 Working at Heights & Formwork Integrity:</strong><br/>
            {proto['heights_safety']}
        </div>
        <div class="protocol-item" style="border-left-color: #10b981;">
            <strong>💧 Worker Health & Occupational Directive:</strong><br/>
            {proto['worker_welfare']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Multi-turn Civil Engineering Assistant Chatbot
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 🤖 2. Construction Engineering & Safety Copilot")
    st.caption("Ask questions on concrete mix designs, stripping times, scaffolding safety, soil shoring, or regulatory codes.")

    # Initialize chat history in session_state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "👋 **Hello Engineer!** I am your **Multimodal Construction Intelligence Copilot**, certified in Indian Standards (IS 456, IS 800, NBC 2016) and OSHA 1926 Safety Regulations. How can I assist with your site operations or structural questions today?"
            }
        ]

    # Quick prompt shortcuts row
    st.markdown("##### 💡 Suggested Engineering Questions:")
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        if st.button("📋 Min. stripping time for beam props per IS 456?", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "What is the minimum stripping time for beam soffits and props per IS 456:2000 Clause 11.3?"
            })
            with st.spinner("Consulting Civil Engineering Knowledge Base..."):
                resp = chat_with_engineering_assistant(
                    conversation_history=st.session_state.chat_messages,
                    api_key=api_key,
                    model_name=model_name,
                    weather_context=selected_weather,
                    force_demo=force_demo
                )
                st.session_state.chat_messages.append({"role": "assistant", "content": resp})
            st.rerun()

        if st.button("🏗️ Scaffolding tie-in rules per OSHA 1926.451?", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "Explain scaffolding safety inspection and tie-in protocol under OSHA 1926.451."
            })
            with st.spinner("Consulting Civil Engineering Knowledge Base..."):
                resp = chat_with_engineering_assistant(
                    conversation_history=st.session_state.chat_messages,
                    api_key=api_key,
                    model_name=model_name,
                    weather_context=selected_weather,
                    force_demo=force_demo
                )
                st.session_state.chat_messages.append({"role": "assistant", "content": resp})
            st.rerun()

    with q_col2:
        if st.button("🧱 How to repair honeycombing in structural columns?", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "How to treat severe honeycombing and cold joints in deep structural columns?"
            })
            with st.spinner("Consulting Civil Engineering Knowledge Base..."):
                resp = chat_with_engineering_assistant(
                    conversation_history=st.session_state.chat_messages,
                    api_key=api_key,
                    model_name=model_name,
                    weather_context=selected_weather,
                    force_demo=force_demo
                )
                st.session_state.chat_messages.append({"role": "assistant", "content": resp})
            st.rerun()

        if st.button("💧 Permissible slump limits for tremie underwater concrete?", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "What is the permissible slump test range for tremie pipe underwater concrete?"
            })
            with st.spinner("Consulting Civil Engineering Knowledge Base..."):
                resp = chat_with_engineering_assistant(
                    conversation_history=st.session_state.chat_messages,
                    api_key=api_key,
                    model_name=model_name,
                    weather_context=selected_weather,
                    force_demo=force_demo
                )
                st.session_state.chat_messages.append({"role": "assistant", "content": resp})
            st.rerun()

    # Render Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            avatar = "👷‍♂️" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # Chat Input Box
    user_input = st.chat_input("Enter your civil engineering or safety query (e.g. M30 mix design, shear links, crane wind limits)...")
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.spinner("Generating engineering consultation..."):
            reply = chat_with_engineering_assistant(
                conversation_history=st.session_state.chat_messages,
                api_key=api_key,
                model_name=model_name,
                weather_context=selected_weather,
                force_demo=force_demo
            )
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # Reset Chat button
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "👋 Chat reset. What structural or site safety query can I help you resolve next?"
            }
        ]
        st.rerun()
