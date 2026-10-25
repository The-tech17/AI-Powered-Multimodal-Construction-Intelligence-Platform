"""Google Gemini API multimodal interface with graceful demonstration mode fallback.
Handles multimodal prompt engineering for construction safety audits, crack diagnostics,
and civil engineering conversational assistant.
"""

import json
import logging
import re
from typing import Optional, Dict, Any, List

# Attempt modern google.genai first, then legacy google.generativeai, then fallback
try:
    from google import genai
    from google.genai import types
    GENAI_CLIENT_AVAILABLE = True
except ImportError:
    GENAI_CLIENT_AVAILABLE = False
    try:
        import google.generativeai as legacy_genai
        LEGACY_GENAI_AVAILABLE = True
    except ImportError:
        LEGACY_GENAI_AVAILABLE = False

from modules.sample_data import (
    SAMPLE_PPE_PHOTOS,
    SAMPLE_CRACK_PHOTOS,
    generate_generic_mock_ppe,
    generate_generic_mock_crack
)

logger = logging.getLogger(__name__)


def clean_json_response(raw_text: str) -> dict:
    """Extract and parse clean JSON from markdown code fences or raw text."""
    text = raw_text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
    text = text.strip()
    
    # Locate outermost JSON braces
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        text = text[start_idx:end_idx + 1]
    
    return json.loads(text)


def analyze_ppe_multimodal(
    image_bytes: bytes,
    mime_type: str = "image/png",
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash",
    sample_key: Optional[str] = None,
    force_demo: bool = False
) -> Dict[str, Any]:
    """Perform multimodal PPE and construction site safety audit.
    Falls back gracefully to demonstration mode if no API key or call fails.
    """
    # Check if forced demo or matching sample
    if force_demo or not api_key or not api_key.strip():
        if sample_key and sample_key in SAMPLE_PPE_PHOTOS:
            result = dict(SAMPLE_PPE_PHOTOS[sample_key]["mock_result"])
            result["_engine"] = "Demonstration Mode (Sample Model)"
            return result
        result = generate_generic_mock_ppe()
        result["_engine"] = "Demonstration Mode (Deterministic Simulation)"
        return result

    # Multimodal prompt with strict JSON schema instructions
    prompt = """You are an expert Certified Safety Professional (CSP) and senior construction safety auditor evaluating a site photograph under OSHA 1926 Safety and Health Regulations for Construction and Indian Standard IS 456 / IS 2925 / IS 15809.

Analyze the provided construction site image thoroughly and output ONLY a valid JSON object with the following exact keys and structure:
{
  "safety_score": integer (0 to 100, where 100 is flawless compliance),
  "overall_status": string (e.g. "Compliant - Low Risk", "Action Required - Moderate Risk", "High Risk - Immediate Intervention Required", or "Critical Non-Compliance"),
  "workers_detected": integer,
  "audit_timestamp": string,
  "ppe_detection": [
    {
      "item": string (e.g. "Industrial Safety Helmets", "High-Visibility Reflective Vests", "Steel-Toe Safety Footwear", "Fall Protection Harnesses"),
      "status": string ("Compliant", "Partial", "Non-Compliant", or "Not Applicable"),
      "compliant_count": integer,
      "total_workers": integer,
      "standard": string (relevant OSHA / IS code),
      "notes": string
    }
  ],
  "identified_hazards": [
    {
      "hazard": string,
      "severity": string ("Low", "Medium", "High", or "Critical"),
      "location": string,
      "osha_citation": string,
      "remedy": string (concrete engineering/administrative corrective action)
    }
  ],
  "recommendations_summary": [
    string (bullet points of priority safety recommendations)
  ]
}

Return purely the raw JSON object without additional conversational filler."""

    try:
        if GENAI_CLIENT_AVAILABLE:
            client = genai.Client(api_key=api_key.strip())
            # Prepare image part
            img_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
            response = client.models.generate_content(
                model=model_name,
                contents=[img_part, prompt],
                config=config
            )
            raw_text = response.text or ""
            data = clean_json_response(raw_text)
            data["_engine"] = f"Live Gemini ({model_name})"
            return data
    except Exception as e:
        logger.warning(f"Live Gemini API PPE analysis failed: {e}. Falling back to demo mode.")

    # Graceful fallback on API error / quota limit
    if sample_key and sample_key in SAMPLE_PPE_PHOTOS:
        result = dict(SAMPLE_PPE_PHOTOS[sample_key]["mock_result"])
    else:
        result = generate_generic_mock_ppe()
    result["_engine"] = "Demonstration Mode (Fallback - API Offline/Exhausted)"
    return result


def analyze_crack_multimodal(
    image_bytes: bytes,
    mime_type: str = "image/png",
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash",
    sample_key: Optional[str] = None,
    force_demo: bool = False
) -> Dict[str, Any]:
    """Perform multimodal crack diagnostics and structural integrity classification.
    Classifies defect type under IS 456:2000 and ACI 224R.
    """
    if force_demo or not api_key or not api_key.strip():
        if sample_key and sample_key in SAMPLE_CRACK_PHOTOS:
            result = dict(SAMPLE_CRACK_PHOTOS[sample_key]["mock_result"])
            result["_engine"] = "Demonstration Mode (Sample Model)"
            return result
        result = generate_generic_mock_crack()
        result["_engine"] = "Demonstration Mode (Deterministic Simulation)"
        return result

    prompt = """You are a senior Chartered Structural Forensic Engineer specializing in concrete pathology, damage forensics, and rehabilitation under Indian Standard IS 456:2000 and ACI 224R-01 (Control of Cracking in Concrete Structures).

Carefully examine this concrete/structural image and diagnose the pathology. Return ONLY a valid JSON object with the following exact keys:
{
  "defect_type": string (Must classify into one of: "Hairline Crack", "Differential Settlement Crack", "Structural Shear Crack", "Thermal Expansion / Contraction", or "Spalling & Reinforcement Delamination"),
  "subtype": string (e.g. "Diagonal Tension Shear in RC Beam", "Carbonation Cover Spall", etc.),
  "crack_width_mm": float (estimated maximum crack width in millimeters),
  "urgency": string (Must be one of: "Immediate Evacuation / Shoring", "Urgent Structural Retrofit", "Moderate Monitoring & Repair", or "Low Routine Maintenance"),
  "risk_score": integer (0 to 100),
  "is_structural": boolean (true if structural load-bearing member affected, false if superficial plaster/finish),
  "is_456_limit_exceeded": boolean (true if crack width > 0.3mm as per IS 456 Clause 35.3.2),
  "is_456_clause": string (relevant IS 456 clause reference and comparison),
  "root_causes": [string (3 detailed technical root causes)],
  "engineering_repairs": [
    {
      "step": integer,
      "action": string,
      "details": string (specification of materials, pressures, methods e.g. low-viscosity epoxy injection, CFRP wrapping, rebar passivation)
    }
  ],
  "repair_materials": string (list of technical repair materials e.g. ASTM C881 epoxy, micro-concrete, SBR bonding agent),
  "monitoring_protocol": string (long-term structural monitoring protocol e.g. Tell-Tale monitors, UPV testing)
}

Return purely the raw JSON object without extra conversational text."""

    try:
        if GENAI_CLIENT_AVAILABLE:
            client = genai.Client(api_key=api_key.strip())
            img_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
            response = client.models.generate_content(
                model=model_name,
                contents=[img_part, prompt],
                config=config
            )
            raw_text = response.text or ""
            data = clean_json_response(raw_text)
            data["_engine"] = f"Live Gemini ({model_name})"
            return data
    except Exception as e:
        logger.warning(f"Live Gemini API Crack analysis failed: {e}. Falling back to demo mode.")

    if sample_key and sample_key in SAMPLE_CRACK_PHOTOS:
        result = dict(SAMPLE_CRACK_PHOTOS[sample_key]["mock_result"])
    else:
        result = generate_generic_mock_crack()
    result["_engine"] = "Demonstration Mode (Fallback - API Offline/Exhausted)"
    return result


def chat_with_engineering_assistant(
    conversation_history: List[Dict[str, str]],
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash",
    weather_context: Optional[str] = None,
    force_demo: bool = False
) -> str:
    """Multi-turn civil and construction safety engineering assistant.
    Provides context-aware responses referencing Indian Standards and OSHA.
    """
    last_user_message = conversation_history[-1]["content"] if conversation_history else ""

    if force_demo or not api_key or not api_key.strip():
        return generate_demo_chat_response(last_user_message, weather_context)

    system_instruction = f"""You are the Chief Civil & Construction Safety Engineering Copilot for the Multimodal Construction Intelligence Platform.
You hold qualifications as a Senior Chartered Structural Engineer (M.I.E., M.I.Struct.E.) and OSHA Certified Safety Auditor.
You provide authoritative, highly technical, and practical construction site guidance referencing:
- Indian Standard IS 456:2000 (Plain & Reinforced Concrete Code of Practice)
- IS 800:2007 (General Construction in Steel)
- National Building Code of India (NBC 2016)
- OSHA 1926 Construction Safety Standards (Subparts C, E, M, P, CC)
- ACI 318, ACI 224R, and ACI 305R/306R

Current Site Environmental Condition: {weather_context or "Normal / Favorable (28°C, calm)"}.

Maintain a professional, structured tone with formulas, numerical tolerances, clause references, and step-by-step checklists where applicable."""

    try:
        if GENAI_CLIENT_AVAILABLE:
            client = genai.Client(api_key=api_key.strip())
            
            # Format contents from conversation history
            contents = []
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
            
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config
            )
            return response.text or "No response received from engineering AI."
    except Exception as e:
        logger.warning(f"Live Gemini Chat failed: {e}. Falling back to demo response.")

    return generate_demo_chat_response(last_user_message, weather_context)


def generate_demo_chat_response(prompt: str, weather_context: Optional[str] = None) -> str:
    """Generate high-quality civil engineering responses for demonstration mode."""
    p_lower = prompt.lower()
    
    if "stripping" in p_lower or "soffit" in p_lower or "formwork" in p_lower or "props" in p_lower or "curing" in p_lower:
        return f"""### 📋 Formwork Stripping & Deshuttering Periods per **IS 456:2000 Clause 11.3**

Under standard OPC cement conditions (temperature > 16°C and moist curing maintained):

| Structural Element | Minimum Period Before Stripping Formwork | Clause Reference |
| :--- | :--- | :--- |
| **Vertical formwork to columns, walls, beams** | 16 to 24 hours | IS 456 Table 11.3.1 |
| **Soffit formwork to slabs** (props immediately refixed) | 3 days | IS 456 Cl. 11.3.1(b) |
| **Soffit formwork to beams** (props immediately refixed) | 7 days | IS 456 Cl. 11.3.1(c) |
| **Props to slabs spanning up to 4.5 m** | 7 days | IS 456 Cl. 11.3.1(d) |
| **Props to slabs spanning over 4.5 m** | 14 days | IS 456 Cl. 11.3.1(d) |
| **Props to beams & arches spanning up to 6 m** | 14 days | IS 456 Cl. 11.3.1(e) |
| **Props to beams & arches spanning over 6 m** | 21 days | IS 456 Cl. 11.3.1(e) |

> ⚠️ **Field Quality Note**: For PPC (Portland Pozzolana) or PSC (Slag) cement, stripping times must be extended by **at least 25% to 30%** due to slower initial pozzolanic hydration rates. Under the current site weather condition (*{weather_context or 'Standard'}*), do not strip until cube compressive test verifies minimum 70% characteristic strength ($f_{ck}$)."""

    elif "scaffold" in p_lower or "osha" in p_lower or "fall" in p_lower or "tie-in" in p_lower:
        return f"""### 🏗️ Scaffolding Safety & Tie-in Protocol per **OSHA 1926.451 & IS 3696**

#### 1. Foundation & Base Support
- Baseplates and mudsills (minimum 2" x 10" structural timber) are mandatory to distribute loads onto soil.
- Screw jacks must not be extended beyond manufacturer tolerance (typically max 12-18 inches).

#### 2. Stability & Tie-in Ratios (OSHA 1926.451(c)(1))
- **Height-to-Base Ratio**: Scaffolds with a height-to-base width ratio greater than **4:1** must be restrained from tipping by guying, tying, or bracing.
- **Vertical Tie Spacing**:
  - Scaffolds <= 3 ft (0.91 m) wide: Vertical tie every **20 ft (6.1 m)**.
  - Scaffolds > 3 ft (0.91 m) wide: Vertical tie every **26 ft (7.9 m)**.
- **Horizontal Tie Spacing**: Ties must be installed at ends and at intervals not exceeding **30 ft (9.1 m)** horizontally.

#### 3. Fall Protection & Guardrail Specifications
- Top-rail: 42" +/- 3" (1.07 m) capable of withstanding **200 lbs (890 N)** outward load.
- Mid-rail: Installed midway (approx 21") capable of withstanding **150 lbs (667 N)**.
- Toe-board: Minimum 3.5" (8.9 cm) height along open edges to eliminate dropped object hazards.
- Full-body harness mandatory if working within 10 ft of unprotected perimeter or when erecting/dismantling."""

    elif "honeycomb" in p_lower or "cold joint" in p_lower or "remedy" in p_lower:
        return """### 🧱 Structural Repair Procedure for Honeycombing & Cold Joints

#### Diagnosis
Honeycombing occurs when coarse aggregates segregate from mortar matrix due to:
1. Insufficient vibration or over-vibration causing paste settlement.
2. Congested reinforcement cages restricting aggregate flow.
3. Leaking formwork joints draining cement slurry.

#### Engineering Rectification Steps (ACI 546R & IS 456):
1. **Delineation & Sounding**: Hammer-tap the affected column zone to identify the full boundary of hollow/unconsolidated concrete.
2. **Saw-cutting**: Saw-cut perimeter to a depth of **12 mm to 15 mm** at right angles to prevent feathered edges.
3. **Pneumatic Chipping**: Chip back loose matrix until solid, sound aggregate is reached (minimum 20 mm clearance behind exposed rebars).
4. **Air-Water Jetting**: Thoroughly clean cavity to remove all dust, carbonation, and loose debris.
5. **Rebar Treatment**: If rust exists, wire-brush to Sa 2.5 and coat with active zinc-rich epoxy primer.
6. **Bonding Layer**: Apply a coat of **Styrene-Butadiene Rubber (SBR)** polymer slurry or structural epoxy bonding agent.
7. **Infill Grouting**:
   - For shallow patches (<40mm): Apply non-shrink thixotropic polymer-modified repair mortar.
   - For deep honeycomb (>50mm): Erect shuttering and gravity-pour/pump **Free-Flowing Micro-Concrete** (compressive strength > 50 MPa at 28 days).
8. **Curing**: Moist cure continuously for 7 days with wet burlap wraps."""

    elif "slump" in p_lower or "tremie" in p_lower or "pump" in p_lower:
        return """### 💧 Concrete Slump & Workability Standards per **IS 456 Clause 7.1**

| Placement Method & Application | Slump Range (mm) | Workability Degree | Typical Water-Binder Ratio |
| :--- | :--- | :--- | :--- |
| **Mass concrete & lightly reinforced sections** | 25 - 75 mm | Low | 0.45 - 0.50 |
| **Heavily reinforced sections, slabs, beams, columns** | 75 - 125 mm | Medium | 0.40 - 0.45 |
| **Pumped concrete** | 100 - 150 mm | High | 0.38 - 0.42 (with Superplasticizer) |
| **Tremie pipe underwater concreting / bored cast-in-situ piles** | 150 - 200 mm | Very High (Self-compacting) | 0.35 - 0.40 (PCE admixtures) |

> 📌 **Tremie Concreting Special Protocol**: Concrete must maintain a minimum slump of **150 mm for at least 2 hours** to prevent pipe clogging. Minimum cementitious content must not be less than **400 kg/m³** to prevent segregation under hydrostatic head."""

    else:
        return f"""### 🏗️ Engineering Advisory & Site Guidance

Regarding your inquiry: **"{prompt}"**

#### Key Engineering Considerations:
1. **Structural & Design Verification**: Always cross-examine loading assumptions against **IS 456:2000** for reinforced concrete structures and **IS 800:2007** for structural steel frames.
2. **Safety Compliance**: Ensure full adherence to **OSHA 1926 Safety & Health Regulations for Construction** and **NBC 2016 Part 7** regarding site management and personnel welfare.
3. **Current Site Meteorological Protocol**:
   - Status: **{weather_context or 'Normal Working Conditions'}**
   - Ensure hydration checks, material strapping, and formwork stability are monitored according to the environmental advisory.

If you have specific dimensions, mix grades (M25, M30, M40), or loading configurations, feel free to supply them for precise numerical calculation."""
