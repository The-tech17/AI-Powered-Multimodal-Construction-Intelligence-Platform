"""Sample data generator and mock multimodal engines for demonstration mode.
Provides high-fidelity simulated inspections, synthetic technical site photos,
and deterministic fallback models when Gemini API key is absent.
"""

import io
from PIL import Image, ImageDraw, ImageFont
import json


def create_synthetic_image(title: str, subtitle: str, theme: str = "safety") -> Image.Image:
    """Generate a high-contrast, informative synthetic site photo representation."""
    width, height = 720, 480
    
    if theme == "safety":
        bg_color = (24, 30, 42)
        grid_color = (38, 48, 66)
        accent_color = (245, 158, 11) # Safety Amber
        text_color = (240, 244, 248)
    elif theme == "shear_crack":
        bg_color = (75, 85, 99) # Concrete Grey
        grid_color = (60, 70, 82)
        accent_color = (239, 68, 68) # Defect Red
        text_color = (255, 255, 255)
    elif theme == "spalling":
        bg_color = (65, 75, 88)
        grid_color = (50, 60, 72)
        accent_color = (180, 83, 9) # Rust/Corrosion
        text_color = (255, 255, 255)
    elif theme == "settlement":
        bg_color = (88, 65, 60) # Brick/Masonry tint
        grid_color = (70, 50, 45)
        accent_color = (234, 88, 12)
        text_color = (255, 255, 255)
    else: # hairline
        bg_color = (140, 145, 150)
        grid_color = (125, 130, 135)
        accent_color = (59, 130, 246)
        text_color = (20, 25, 30)

    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw structural grid lines
    step = 40
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # Theme-specific illustrations
    if theme == "safety":
        # Draw Scaffolding frame
        draw.rectangle([(80, 120), (640, 420)], outline=(100, 116, 139), width=4)
        draw.line([(80, 120), (640, 420)], fill=(71, 85, 105), width=2)
        draw.line([(80, 420), (640, 120)], fill=(71, 85, 105), width=2)
        draw.line([(80, 270), (640, 270)], fill=(100, 116, 139), width=3)
        
        # Worker 1: Unanchored at height
        draw.ellipse([(220, 160), (260, 200)], fill=(239, 68, 68)) # Missing helmet - red alert
        draw.rectangle([(215, 200), (265, 260)], fill=(245, 158, 11)) # High-vis vest
        draw.line([(240, 260), (225, 320)], fill=(30, 41, 59), width=6) # Legs
        draw.line([(240, 260), (255, 320)], fill=(30, 41, 59), width=6)
        
        # Danger marker
        draw.rectangle([(275, 160), (450, 195)], fill=(220, 38, 38))
        
        # Worker 2: Compliant ground level
        draw.ellipse([(480, 290), (520, 330)], fill=(255, 255, 255)) # White Hardhat
        draw.rectangle([(475, 330), (525, 390)], fill=(16, 185, 129)) # Green Safety vest
        draw.line([(500, 390), (485, 440)], fill=(30, 41, 59), width=6)
        draw.line([(500, 390), (515, 440)], fill=(30, 41, 59), width=6)

    elif theme == "shear_crack":
        # Reinforced concrete beam representation
        draw.rectangle([(40, 140), (680, 340)], fill=(90, 100, 115), outline=(148, 163, 184), width=3)
        # 45 degree diagonal shear crack path
        crack_points = [
            (260, 340), (290, 300), (320, 265), (350, 225), (390, 185), (420, 140)
        ]
        draw.line(crack_points, fill=(15, 23, 42), width=7)
        # Crack width dimension callout
        draw.line([(320, 265), (440, 265)], fill=(239, 68, 68), width=2)
        draw.rectangle([(440, 250), (620, 280)], fill=(185, 28, 28))

    elif theme == "spalling":
        # Wall surface with spall pocket
        draw.rectangle([(60, 100), (660, 380)], fill=(80, 90, 105), outline=(100, 116, 139), width=2)
        # Irregular spalled depression
        draw.polygon([(240, 160), (480, 170), (520, 300), (450, 340), (220, 320)], fill=(45, 52, 63))
        # Exposed corroded rebar mesh
        for rx in [290, 350, 410, 460]:
            draw.line([(rx, 175), (rx, 315)], fill=(180, 83, 9), width=5) # Rust brown rebar
        draw.line([(250, 220), (490, 220)], fill=(180, 83, 9), width=5)
        draw.line([(250, 270), (490, 270)], fill=(180, 83, 9), width=5)

    elif theme == "settlement":
        # Brick wall pattern with stepped diagonal crack
        for row in range(5, 17):
            y_pos = row * 22
            draw.line([(60, y_pos), (660, y_pos)], fill=(120, 90, 80), width=2)
        # Stepped fracture
        step_pts = [(180, 370), (220, 370), (220, 320), (270, 320), (270, 270), 
                    (330, 270), (330, 220), (390, 220), (390, 160), (450, 160), (450, 110)]
        draw.line(step_pts, fill=(20, 15, 15), width=6)

    else: # hairline
        # Smooth plaster surface with fine spiderweb/shrinkage crack
        pts = [(140, 240), (200, 235), (280, 245), (360, 230), (450, 250), (550, 240), (620, 245)]
        draw.line(pts, fill=(60, 65, 75), width=2)

    # Technical Header Overlay
    draw.rectangle([(0, 0), (width, 70)], fill=(15, 23, 42))
    draw.rectangle([(0, 67), (width, 70)], fill=accent_color)
    
    # Try basic font or default
    try:
        font_lg = ImageFont.truetype("arial.ttf", 22)
        font_sm = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font_lg = ImageFont.load_default()
        font_sm = ImageFont.load_default()

    draw.text((20, 14), title.upper(), fill=text_color, font=font_lg)
    draw.text((20, 42), f"DIAGNOSTIC TELEMETRY • {subtitle}", fill=(148, 163, 184), font=font_sm)

    # Watermark Footer
    draw.rectangle([(0, height - 35), (width, height)], fill=(15, 23, 42))
    draw.text((20, height - 25), "MULTIMODAL CIVIL VISION ENGINE • CAPSTONE VERIFIED", fill=(100, 116, 139), font=font_sm)
    draw.text((width - 190, height - 25), "OSHA / IS 456 STANDARDS", fill=accent_color, font=font_sm)

    return img


def get_image_bytes(img: Image.Image) -> bytes:
    """Convert PIL image to PNG bytes."""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# Preset Sample Images
SAMPLE_PPE_PHOTOS = {
    "Scaffolding Staging - Missing Fall Harness & Helmet": {
        "title": "High-Rise Scaffolding Staging",
        "subtitle": "Elevation 14.5m • Bay 4 • Working at Heights",
        "theme": "safety",
        "mock_result": {
            "safety_score": 58,
            "overall_status": "High Risk - Immediate Intervention Required",
            "workers_detected": 2,
            "audit_timestamp": "2026-10-25 15:45 IST",
            "ppe_detection": [
                {
                    "item": "Industrial Safety Helmets",
                    "status": "Non-Compliant",
                    "compliant_count": 1,
                    "total_workers": 2,
                    "standard": "OSHA 1926.100 / IS 2925",
                    "notes": "1 worker operating on upper tier without mandatory Class E protective helmet."
                },
                {
                    "item": "High-Visibility Reflective Vests",
                    "status": "Compliant",
                    "compliant_count": 2,
                    "total_workers": 2,
                    "standard": "IS 15809:2017 / ANSI 107",
                    "notes": "Both workers wearing retro-reflective fluorescent class 2 vests."
                },
                {
                    "item": "Steel-Toe Safety Footwear",
                    "status": "Compliant",
                    "compliant_count": 2,
                    "total_workers": 2,
                    "standard": "IS 15298:2016",
                    "notes": "Slip-resistant puncture-proof toe cap boots verified on platform."
                },
                {
                    "item": "Fall Arrest Harness & Lanyard",
                    "status": "Critical Violation",
                    "compliant_count": 0,
                    "total_workers": 1,
                    "standard": "OSHA 1926.502 / IS 3521",
                    "notes": "Worker exposed to unprotected perimeter >2.8m without anchored full-body harness."
                }
            ],
            "identified_hazards": [
                {
                    "hazard": "Unanchored Worker at Elevated Scaffold Perimeter",
                    "severity": "Critical",
                    "location": "Upper staging tier, scaffolding bay 4",
                    "osha_citation": "OSHA 1926.501(b)(1) & IS 3696 Part 1",
                    "remedy": "Issue immediate Stop-Work Order. Mandate twin-tail shock-absorbing lanyard tied off to 22.2 kN (5,000 lbs) certified anchor lifeline before work resumes."
                },
                {
                    "hazard": "Missing Head Protection Underneath Staging",
                    "severity": "High",
                    "location": "Intermediate planking level",
                    "osha_citation": "OSHA 1926.100(a) & IS 2925",
                    "remedy": "Equip worker with IS 2925 Type 1 industrial helmet with 4-point chin strap fastened. Install toe-boards to prevent falling tool hazards."
                },
                {
                    "hazard": "Missing Guardrail Mid-Rail & Toe-board",
                    "severity": "Medium",
                    "location": "Scaffold working deck edge",
                    "osha_citation": "OSHA 1926.451(g)(1)",
                    "remedy": "Install standard top-rail at 42 inches and mid-rail at 21 inches along all open scaffold faces."
                }
            ],
            "recommendations_summary": [
                "Conduct mandatory 15-minute Working-at-Heights safety stand-down for Scaffolding Crew B.",
                "Verify third-party scaffolding fitness tag (Green Tag) signed by competent scaffolding supervisor.",
                "Deploy debris netting along outer scaffolding envelope per NBC 2016 Part 7."
            ]
        }
    },
    "Trench Excavation Crew - Fully Compliant PPE": {
        "title": "Deep Trench Shoring & Dewatering",
        "subtitle": "Depth 3.2m • Shoring Box • Ground Support Crew",
        "theme": "safety",
        "mock_result": {
            "safety_score": 96,
            "overall_status": "Fully Compliant - Low Risk Benchmark",
            "workers_detected": 4,
            "audit_timestamp": "2026-10-25 15:48 IST",
            "ppe_detection": [
                {
                    "item": "Industrial Safety Helmets",
                    "status": "Compliant",
                    "compliant_count": 4,
                    "total_workers": 4,
                    "standard": "OSHA 1926.100 / IS 2925",
                    "notes": "All crew members wearing properly adjusted Type 1 Class C/E hard hats with chin straps."
                },
                {
                    "item": "High-Visibility Reflective Vests",
                    "status": "Compliant",
                    "compliant_count": 4,
                    "total_workers": 4,
                    "standard": "IS 15809:2017 / ANSI 107",
                    "notes": "Class 3 high-vis reflective apparel visible under varied ambient excavation lighting."
                },
                {
                    "item": "Steel-Toe Safety Footwear",
                    "status": "Compliant",
                    "compliant_count": 4,
                    "total_workers": 4,
                    "standard": "IS 15298:2016",
                    "notes": "Waterproof heavy-duty gumboots with composite steel-toe protection in place."
                },
                {
                    "item": "Trench Shoring & Egress Ladder",
                    "status": "Compliant",
                    "compliant_count": 4,
                    "total_workers": 4,
                    "standard": "OSHA 1926.651 / IS 3764",
                    "notes": "Aluminum hydraulic trench shield and secured extension ladder within 25ft of workers."
                }
            ],
            "identified_hazards": [
                {
                    "hazard": "Minor Soil Spoil Pile Proximity",
                    "severity": "Low",
                    "location": "Trench lip east perimeter",
                    "osha_citation": "OSHA 1926.651(j)(2) / IS 3764",
                    "remedy": "Ensure all excavated spoil soil is pushed back at least 2 feet (0.6 meters) from the trench lip."
                }
            ],
            "recommendations_summary": [
                "Maintain continuous dewatering pump operations to prevent slope liquefaction.",
                "Conduct daily morning atmospheric gas testing before trench entry (O2, H2S, LEL)."
            ]
        }
    }
}

SAMPLE_CRACK_PHOTOS = {
    "45° Diagonal Shear Crack in Reinforced Concrete Beam": {
        "title": "RC Transfer Girder Beam Shear Diagnostic",
        "subtitle": "Span Support Joint • Diagonal Tension • Span L/4",
        "theme": "shear_crack",
        "mock_result": {
            "defect_type": "Structural Shear Crack",
            "subtype": "Diagonal Tension Shear Failure in RC Beam",
            "crack_width_mm": 3.2,
            "urgency": "Urgent Structural Retrofit",
            "risk_score": 88,
            "is_structural": True,
            "is_456_limit_exceeded": True,
            "is_456_clause": "IS 456:2000 Clause 35.3.2 & Clause 40 (Shear Limit 0.3mm exceeded by 10.6x)",
            "root_causes": [
                "Principal tensile stress exceeds diagonal shear capacity of concrete under heavy live load.",
                "Inadequate stirrup shear rebar spacing or insufficient shear links near column support zone.",
                "Possible settlement of adjacent supporting column producing differential shear displacement."
            ],
            "engineering_repairs": [
                {
                    "step": 1,
                    "action": "Immediate Temporary Shoring",
                    "details": "Install heavy-duty adjustable Acrow steel props under beam at 1.0m c/c to relieve dead load immediately."
                },
                {
                    "step": 2,
                    "action": "Pressure Low-Viscosity Epoxy Injection",
                    "details": "Seal crack surface with thixotropic epoxy paste, install injection nipples at 150mm intervals, and inject low-viscosity resin (viscosity <150 mPa.s) at 0.3 to 0.5 MPa pressure."
                },
                {
                    "step": 3,
                    "action": "Carbon Fiber (CFRP) Shear Strengthening",
                    "details": "Bond bidirectional Carbon Fiber Reinforced Polymer (CFRP) U-wraps (300 g/m²) across the shear zone with structural epoxy saturant per ACI 440.2R."
                }
            ],
            "repair_materials": "Low-viscosity structural epoxy (ASTM C881 Type I/IV), CFRP composite fabric, Thixotropic capping sealant",
            "monitoring_protocol": "Install Tell-Tale acrylic crack motion monitors and ultrasonic pulse velocity (UPV) grid testing post-curing."
        }
    },
    "Concrete Retaining Wall Spalling with Corroded Rebar": {
        "title": "Subterranean Retaining Wall Spalling",
        "subtitle": "Basement Tier -2 • Delamination • Rebar Oxidation",
        "theme": "spalling",
        "mock_result": {
            "defect_type": "Spalling & Reinforcement Delamination",
            "subtype": "Chloride & Carbonation Induced Concrete Spall",
            "crack_width_mm": 5.8,
            "urgency": "Urgent Structural Retrofit",
            "risk_score": 82,
            "is_structural": True,
            "is_456_limit_exceeded": True,
            "is_456_clause": "IS 456:2000 Clause 26.4 (Loss of Nominal Concrete Cover & Rebar Passivity)",
            "root_causes": [
                "Carbonation front reaching rebar level, lowering concrete alkalinity (pH < 9).",
                "Moisture & chloride ingress causing volumetric expansion of iron oxide (2-6x volume increase), blowing off concrete cover.",
                "Inadequate clear cover during casting (<25mm in underground earth-retaining environment)."
            ],
            "engineering_repairs": [
                {
                    "step": 1,
                    "action": "Chipping & Mechanical Concrete Breakout",
                    "details": "Saw-cut edges at 90° angle to 15mm depth. Chip back loose and carbonated concrete 20mm behind exposed rebar."
                },
                {
                    "step": 2,
                    "action": "Rebar De-rusting & Anti-Corrosion Passivation",
                    "details": "Grit-blast corroded rebar to Sa 2.5 standard. Apply two coats of active zinc-rich epoxy primer (ASTM D520)."
                },
                {
                    "step": 3,
                    "action": "Polymer Modified Structural Mortar Patching",
                    "details": "Apply bonding agent (SBR polymer/epoxy), then build up shrinkage-compensated fiber-reinforced repair mortar in 25mm layers to original profile."
                }
            ],
            "repair_materials": "Zinc-rich rebar primer, Styrene Butadiene Rubber (SBR) bonding slurry, Class R4 thixotropic structural repair mortar",
            "monitoring_protocol": "Half-cell potential electrochemical mapping (ASTM C876) every 6 months to track rebar corrosion activity."
        }
    },
    "Brick Infill Wall Differential Settlement Crack": {
        "title": "External Infill Masonry Settlement",
        "subtitle": "Grade Beam Level • Stepped Shear Fracture • Southwest Corner",
        "theme": "settlement",
        "mock_result": {
            "defect_type": "Settlement Fracture",
            "subtype": "Stepped Diagonal Differential Foundation Settlement",
            "crack_width_mm": 4.1,
            "urgency": "Moderate Monitoring & Repair",
            "risk_score": 64,
            "is_structural": True,
            "is_456_limit_exceeded": True,
            "is_456_clause": "IS 1905:1987 (Structural Masonry Code) & IS 456 Clause 35.3",
            "root_causes": [
                "Uneven foundation consolidation or moisture fluctuations in expansive black cotton subsoil.",
                "Differential settlement exceeding 1/500 angular distortion tolerance.",
                "Absence of plinth tie beam or inadequate foundation soil bearing capacity."
            ],
            "engineering_repairs": [
                {
                    "step": 1,
                    "action": "Geotechnical Subsoil Grouting",
                    "details": "Conduct low-pressure cement-bentonite permeation grouting below corner footing to consolidate foundation subgrade."
                },
                {
                    "step": 2,
                    "action": "Stainless Steel Stitching Pins",
                    "details": "Rake horizontal bed joints 500mm on either side of crack. Bed 6mm ribbed stainless steel helical bars in high-strength epoxy grout at 300mm vertical intervals."
                },
                {
                    "step": 3,
                    "action": "Flexible Polyurethane Joint Sealing",
                    "details": "Seal exterior joint with elastomeric polyurethane sealant to allow minor cyclic thermal breathing without moisture ingress."
                }
            ],
            "repair_materials": "Helical stainless steel stitching rods, Non-shrink cementitious foundation grout, Polyurethane elastomeric sealant",
            "monitoring_protocol": "Geotechnical settlement markers and optical leveling surveys over 90 days to verify settlement stabilization."
        }
    },
    "Plaster Hairline Thermal Shrinkage Crack": {
        "title": "Internal Partition Wall Plaster Inspection",
        "subtitle": "East Facing Living Area • Fine Surface Fissures",
        "theme": "hairline",
        "mock_result": {
            "defect_type": "Hairline Crack",
            "subtype": "Non-Structural Plastic Shrinkage & Thermal Crazing",
            "crack_width_mm": 0.25,
            "urgency": "Low Routine Maintenance",
            "risk_score": 18,
            "is_structural": False,
            "is_456_limit_exceeded": False,
            "is_456_clause": "IS 456:2000 Clause 35.3.2 (Crack width 0.25mm is within 0.3mm permissible design limit)",
            "root_causes": [
                "Rapid surface water evaporation during plaster curing stage (inadequate moist curing).",
                "Thermal expansion differential between RCC slab and clay brick infill masonry.",
                "Rich cement-to-sand plaster mix ratio (1:3) with high shrinkage coefficient."
            ],
            "engineering_repairs": [
                {
                    "step": 1,
                    "action": "Surface V-Groove Raking",
                    "details": "Rake crack into a clean 5mm V-groove with mechanical scraper to remove loose dust and friable particles."
                },
                {
                    "step": 2,
                    "action": "Elastomeric Acrylic Crack Filler",
                    "details": "Press flexible acrylic latex crack filler into groove using putty knife. Reinforce with 50mm glass fiber mesh tape."
                },
                {
                    "step": 3,
                    "action": "Primer & Breathable Emulsion Coat",
                    "details": "Sand flush with 180-grit paper, apply alkali-resistant primer and two coats of elastomeric exterior/interior acrylic paint."
                }
            ],
            "repair_materials": "Flexible acrylic crack paste, 50mm alkali-resistant fiberglass scrim tape, Acrylic masonry primer",
            "monitoring_protocol": "Annual routine visual inspection during post-monsoon repainting cycle."
        }
    }
}


def generate_generic_mock_ppe(filename: str = "Uploaded Image") -> dict:
    """Generate generic realistic PPE audit result for user-uploaded site images."""
    return {
        "safety_score": 74,
        "overall_status": "Moderate Risk - Action Required",
        "workers_detected": 3,
        "audit_timestamp": "2026-10-25 15:52 IST",
        "ppe_detection": [
            {
                "item": "Industrial Safety Helmets (Hard Hats)",
                "status": "Partial",
                "compliant_count": 2,
                "total_workers": 3,
                "standard": "OSHA 1926.100 / IS 2925",
                "notes": "2 workers compliant with white safety helmets; 1 worker observed with missing headgear."
            },
            {
                "item": "High-Visibility Reflective Vests",
                "status": "Compliant",
                "compliant_count": 3,
                "total_workers": 3,
                "standard": "IS 15809:2017 / ANSI 107",
                "notes": "Fluorescent high-vis orange/yellow vests verified on all detected active personnel."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "status": "Partial",
                "compliant_count": 2,
                "total_workers": 3,
                "standard": "IS 15298:2016",
                "notes": "1 worker wearing non-reinforced sport shoes near material unloading zone."
            },
            {
                "item": "Fall Protection / Harnesses",
                "status": "Not Applicable",
                "compliant_count": 0,
                "total_workers": 0,
                "standard": "OSHA 1926.502 / IS 3521",
                "notes": "Workers operating on grade level (<1.8m fall hazard threshold)."
            }
        ],
        "identified_hazards": [
            {
                "hazard": "Missing Hard Hat in Active Material Handling Zone",
                "severity": "High",
                "location": "Ground staging area near material hoist",
                "osha_citation": "OSHA 1926.100(a) / IS 2925",
                "remedy": "Direct worker to immediately don an IS 2925 approved Type 1 Class C/E helmet. Restrict unauthorized entry without full PPE kit."
            },
            {
                "hazard": "Non-Compliant Footwear Exposed to Crushing Hazards",
                "severity": "Medium",
                "location": "Rebar sorting yard",
                "osha_citation": "OSHA 1926.96 / IS 15298",
                "remedy": "Supply steel-toe footwear with 200J impact resistance and puncture-resistant midsole."
            }
        ],
        "recommendations_summary": [
            "Conduct safety induction refresh on head and foot protection guidelines.",
            "Establish strict security checkpoint at entry gate enforcing complete PPE pass."
        ]
    }


def generate_generic_mock_crack(filename: str = "Uploaded Image") -> dict:
    """Generate generic realistic crack diagnostic result for user-uploaded structural images."""
    return {
        "defect_type": "Structural Shear Crack",
        "subtype": "Inclined Concrete Fissure in Load-Bearing Element",
        "crack_width_mm": 1.85,
        "urgency": "Urgent Structural Retrofit",
        "risk_score": 76,
        "is_structural": True,
        "is_456_limit_exceeded": True,
        "is_456_clause": "IS 456:2000 Clause 35.3.2 (Crack width 1.85mm exceeds maximum limit of 0.3mm)",
        "root_causes": [
            "Diagonal tension shear stress exceeding tensile capacity of concrete section.",
            "Combined effect of dead load, dynamic vibration, and minor thermal cycling.",
            "Potential stress concentration near opening or beam-column intersection."
        ],
        "engineering_repairs": [
            {
                "step": 1,
                "action": "Surface Preparation & Port Fixing",
                "details": "Clean crack path with compressed air, grind concrete surface clean, and fix injection ports with fast-setting epoxy."
            },
            {
                "step": 2,
                "action": "Pressure Resin Grouting",
                "details": "Inject low-viscosity structural epoxy under 0.2 to 0.4 MPa pressure starting from lowest port until resin flows from adjacent port."
            },
            {
                "step": 3,
                "action": "Structural Wrapping Reinforcement",
                "details": "Apply unidirectional carbon fiber reinforced polymer (CFRP) wrap across the fissure to restore shear integrity."
            }
        ],
        "repair_materials": "Structural epoxy injection resin (ASTM C881), CFRP fabric, Surface capping epoxy",
        "monitoring_protocol": "Install demec mechanical strain gauges or optical crack monitors for bi-weekly monitoring over 6 months."
    }
