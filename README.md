# 🏗️ Multimodal Construction Intelligence Platform
### Skill Wallet Capstone Project 1 • Production-Ready Autonomous Civil & Safety Engineering AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![OSHA Compliant](https://img.shields.io/badge/Safety%20Standard-OSHA%201926-orange.svg)](https://www.osha.gov/)
[![IS Standard](https://img.shields.io/badge/Civil%20Code-IS%20456%3A2000-green.svg)](https://www.bis.gov.in/)

The **Multimodal Construction Intelligence Platform** is an enterprise-grade AI operating system for modern civil engineering, site safety enforcement, forensic defect diagnostics, techno-economic CapEx planning, and meteorological hazard mitigation.

---

## 🌟 Key Modules & Core Architecture

### 1. 🛡️ Tab 1 - Site Safety & PPE Audit (Epic 2)
- **Multimodal Visual Audit**: Ingests high-resolution construction site photographs (scaffolding, excavations, rebar yards).
- **Standards-Compliant PPE Verification**: Real-time detection and verification of:
  - Safety Helmets / Hard Hats (**OSHA 1926.100 / IS 2925**)
  - High-Visibility Warning Clothes (**IS 15809 / ANSI 107**)
  - Protective Steel-Toe Footwear (**IS 15298**)
  - Fall Arrest Harnesses & Anchorage Points (**OSHA 1926.502 / IS 3521**)
- **Structured JSON Telemetry**: Outputs normalized `safety_score` (0–100), overall risk tier, worker detection census, and identified site hazards with severity ratings (`Critical`, `High`, `Medium`, `Low`).
- **Remediation Action Items**: Prescribes instant corrective administrative and engineering controls with specific OSHA citations.
- **Reporting**: 1-click downloadable structured JSON report and Executive Safety Compliance Certificate (.txt).

### 2. 🔍 Tab 2 - Crack Diagnostics & Structural Integrity (Epic 2)
- **Pathology Classification**: Analyzes concrete member surfaces and classifies defect typology:
  - **Structural Shear Cracks** (45° diagonal tension near supports)
  - **Spalling & Reinforcement Delamination** (carbonation/chloride cover failure)
  - **Differential Foundation Settlement Fractures** (stepped diagonal cracks)
  - **Thermal Expansion / Contraction Cracking**
  - **Superficial Hairline Shrinkage Fissures** (< 1.0mm)
- **Crack Geometry & Tolerance Check**: Measures estimated crack width in millimeters and evaluates against **IS 456:2000 Clause 35.3.2** permissible limit (0.3 mm for moderate exposure, 0.2 mm for severe/marine).
- **Engineering Rehabilitation Specifications**: Step-by-step repair protocols (low-viscosity pressure epoxy injection, CFRP composite wraps, zinc-rich rebar passivation, micro-concreting).
- **Diagnostic Export**: Downloadable forensic structural reports and JSON telemetry.

### 3. 📐 Tab 3 - Planning & Real Estate Valuation (Epic 3)
- **Techno-Economic Modeling**: Configurable structure types (*Residential High-Rise, Commercial IT Complex, Industrial Logistics Warehouse, Luxury Villa Estate, Infrastructure Bridge*).
- **Location Tiers**: Tailored multipliers for Indian metro dynamics (Tier 1: Mumbai, Delhi-NCR, Bengaluru; Tier 2: Pune, Ahmedabad, Chennai; Tier 3: Developing corridors).
- **Budgeting & Asset Valuation**:
  - Total project budget in INR (**Lakhs and Crores** with Indian numbering).
  - CapEx incurred to date vs. remaining capital requirements.
  - Current market equity asset valuation factoring completion appreciation.
- **Civil Material Takeoffs**: Indian standard material estimations for Fe500D TMT steel (MT), OPC/PPC cement (50kg bags), RMC volume (m³), and manufactured sand (CFT/Brass).
- **Milestone Progress Tracker**: Visual 5-phase execution progress bar (Substructure, Superstructure, MEP, Finishes, Handover).
- **Generative 3D Architectural Rendering**: Integrates **Pollinations AI** neural image synthesis to generate hyper-realistic 3D architectural facade renders from geometric parameters.

### 4. 🌦️ Tab 4 - Daily Site Assistant & Weather-Aware Advisory (Epic 5)
- **Dynamic Meteorological Directives**: Adapts safety protocols based on real-time site conditions:
  - *High Wind (>45 km/h)*: Mandatory tower crane cessation (OSHA 1926.1431), weather-vaning jibs, and scaffolding height restrictions.
  - *Heavy Monsoon Rain*: Exterior pour suspension, low-voltage distribution board isolation, trench dewatering.
  - *Extreme Heat (>42°C)*: Hot-weather concreting hydration retarders (ACI 305R / IS 7861), wet burlap curing cycles, OSHA heat stroke hydration rests.
  - *Severe Thunderstorm / Lightning*: 30-30 lightning rule, crane grounding, and steel frame evacuation.
- **Interactive Multi-Turn Civil Engineering Copilot**:
  - Conversational AI powered by Gemini with civil engineering system context.
  - Pre-configured quick-prompt shortcuts for IS 456 stripping periods, OSHA scaffolding tie-ins, column honeycombing repair, and tremie underwater slump limits.

---

## 🏛️ System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit UI Layer                     │
│  (Glassmorphism CSS, Metric Cards, Status Badges, Tabs)     │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
┌──────────────▼──────────────┐ ┌──────────────▼──────────────┐
│   Tab 1 & Tab 2: Multimodal │ │  Tab 3 & Tab 4: Planning &  │
│   Vision & Diagnostics      │ │  Advisory Copilot           │
└──────────────┬──────────────┘ └──────────────┬──────────────┘
               │                               │
┌──────────────▼───────────────────────────────▼──────────────┐
│           Google Gemini API Engine (google.genai)           │
│        (gemini-2.5-flash / gemini-1.5-pro / gemini-2.0)     │
│        + Graceful Zero-Key Demonstration Mode Engine        │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
┌──────────────▼──────────────┐ ┌──────────────▼──────────────┐
│   Governed Standards Engine │ │   Generative 3D Visualizer  │
│   • OSHA 1926 Subparts E/M  │ │   • Pollinations AI Neural  │
│   • IS 456:2000 & IS 800    │ │     Architectural Renderer  │
│   • NBC 2016 Part 7         │ │                             │
└─────────────────────────────┘ └─────────────────────────────┘
```

---

## 🚀 Quickstart & Local Installation

### Prerequisites
- Python 3.10 or higher
- (Optional) Google AI Studio Gemini API Key

### 1. Clone or Download Repository
```bash
git clone https://github.com/your-username/multimodal-construction-intelligence.git
cd "multimodal-construction-intelligence"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
The application will open automatically at `http://localhost:8501`.

---

## ☁️ 1-Click Deployment to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and log in.
3. Click **"New App"** and select:
   - **Repository**: Your repository name
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. (Optional) In **Advanced settings**, add your `GEMINI_API_KEY` under Secrets:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
5. Click **"Deploy"**! The application will deploy in under 60 seconds with **zero external database dependencies**.

---

## 🔐 Demonstration Mode & Offline Resiliency

The platform includes a **built-in high-fidelity Demonstration Mode**:
- If no Gemini API key is supplied, the platform automatically activates realistic synthetic models with benchmark site imagery and certified diagnostic telemetry.
- Users can test all 4 tabs with 100% feature availability without an API key or when offline.
- Supplying a valid Gemini API key in the sidebar unlocks live, real-time multimodal vision inference.

---

## 📜 Governed Standards & References
- **OSHA 1926**: Safety and Health Regulations for Construction (Subparts E, M, P, CC).
- **IS 456:2000**: Code of Practice for Plain and Reinforced Concrete.
- **IS 2925:1984**: Specification for Industrial Safety Helmets.
- **IS 15809:2017**: High Visibility Warning Clothes.
- **IS 15298:2016**: Personal Protective Equipment - Safety Footwear.
- **ACI 224R-01**: Control of Cracking in Concrete Structures.
- **NBC 2016**: National Building Code of India (Part 7: Construction Management).

---

*Engineered as Capstone Project 1 for Skill Wallet Certification.*
