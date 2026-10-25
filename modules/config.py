"""Configuration constants, Indian Standards, and OSHA regulatory references.
Multimodal Construction Intelligence Platform.
"""

APP_TITLE = "Multimodal Construction Intelligence Platform"
APP_SUBTITLE = "Skill Wallet Capstone Project 1 • Autonomous Multimodal Civil & Safety Engineering AI"
VERSION = "1.0.0-PROD"

# Engineering Standards References
STANDARDS = {
    "OSHA_PPE": "OSHA 1926 Subpart E (Personal Protective & Life Saving Equipment)",
    "OSHA_FALL": "OSHA 1926 Subpart M (Fall Protection Criteria & Practices)",
    "OSHA_CRANE": "OSHA 1926 Subpart CC (Cranes & Derricks in Construction)",
    "IS_456": "IS 456:2000 (Plain and Reinforced Concrete - Code of Practice)",
    "IS_2925": "IS 2925:1984 (Specification for Industrial Safety Helmets)",
    "IS_15809": "IS 15809:2017 (High Visibility Warning Clothes)",
    "IS_15298": "IS 15298:2016 (Personal Protective Equipment - Safety Footwear)",
    "IS_3521": "IS 3521:1999 (Industrial Safety Belts and Harnesses)",
    "NBC_2016": "National Building Code of India 2016 (Part 7: Construction Management)",
    "ACI_224R": "ACI 224R-01 (Control of Cracking in Concrete Structures)"
}

# Real Estate & Construction Cost Benchmarks in India (INR / Sq Ft)
COST_BENCHMARKS = {
    "Residential High-Rise": {
        "Standard": 2350,
        "Premium": 3200,
        "Ultra-Luxury": 4600,
        "steel_per_sqft_kg": 4.5,
        "cement_per_sqft_bags": 0.44,
        "sand_per_sqft_cft": 1.75,
        "aggregate_per_sqft_cft": 1.35
    },
    "Commercial IT Complex": {
        "Standard": 2800,
        "Premium": 3900,
        "Ultra-Luxury": 5400,
        "steel_per_sqft_kg": 5.2,
        "cement_per_sqft_bags": 0.48,
        "sand_per_sqft_cft": 1.85,
        "aggregate_per_sqft_cft": 1.45
    },
    "Industrial Logistics Warehouse": {
        "Standard": 1750,
        "Premium": 2300,
        "Ultra-Luxury": 3100,
        "steel_per_sqft_kg": 3.8,
        "cement_per_sqft_bags": 0.36,
        "sand_per_sqft_cft": 1.40,
        "aggregate_per_sqft_cft": 1.20
    },
    "Luxury Villa Estate": {
        "Standard": 3100,
        "Premium": 4400,
        "Ultra-Luxury": 6500,
        "steel_per_sqft_kg": 4.8,
        "cement_per_sqft_bags": 0.46,
        "sand_per_sqft_cft": 1.80,
        "aggregate_per_sqft_cft": 1.40
    },
    "Infrastructure Bridge & Flyover": {
        "Standard": 4800,
        "Premium": 6200,
        "Ultra-Luxury": 8500,
        "steel_per_sqft_kg": 7.5,
        "cement_per_sqft_bags": 0.65,
        "sand_per_sqft_cft": 2.20,
        "aggregate_per_sqft_cft": 1.85
    }
}

# Location Tier Multipliers (Reflecting land cost, labor rates & supply chain logistics in India)
LOCATION_TIERS = {
    "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Hyderabad)": {
        "multiplier": 1.35,
        "market_val_multiplier": 2.80,
        "desc": "High-density metropolitan zones with premium land and labor dynamics."
    },
    "Tier 2 (Pune, Ahmedabad, Chennai, Kolkata, Jaipur, Chandigarh)": {
        "multiplier": 1.15,
        "market_val_multiplier": 2.10,
        "desc": "Major state capitals and expanding commercial hubs."
    },
    "Tier 3 (Tier 3 Municipalities & Industrial Corridors)": {
        "multiplier": 1.00,
        "market_val_multiplier": 1.65,
        "desc": "Emerging growth regions with standard resource costs."
    }
}

# Project Milestone Phases
CONSTRUCTION_MILESTONES = [
    {"name": "Substructure & Deep Foundations", "range": (0, 20), "desc": "Piling, raft excavation, waterproofing & grade beams."},
    {"name": "RCC Superstructure Framing", "range": (20, 50), "desc": "Columns, shear walls, post-tensioned slabs & core shuttering."},
    {"name": "Masonry, MEP & Firefighting", "range": (50, 70), "desc": "AAC blockwork, conduits, plumbing risers, HVAC ducting."},
    {"name": "Finishing, Glazing & Flooring", "range": (70, 90), "desc": "Curtain walls, vitrified tiling, gypsum plaster, paint primer."},
    {"name": "Commissioning, Snagging & OC Handover", "range": (90, 100), "desc": "Lift testing, fire NOC, final snag clearance & client handover."}
]
