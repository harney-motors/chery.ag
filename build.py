#!/usr/bin/env python3
"""
Chery Antigua — static site generator.

Edit the SITE and MODELS data below, then run:  python3 build.py
It writes index.html and models/<slug>.html. CSS/JS live in /assets and are
hand-edited (not generated). Images live in /images.

Design system follows the official Chery regional template (cherysxm.com /
cheryinternational.com): Poppins, light #f4f4f4 backgrounds, deep Chery
navy #0B457F, champagne-bronze #A4896C CTAs, dark performance bands and
big italic uppercase model wordmarks.
"""
import datetime, html, json, pathlib, re

ROOT = pathlib.Path(__file__).parent

# ─────────────────────────────────────────────────────────────── site config
SITE = {
    "brand": "CHERY",
    "sub": "ANTIGUA",
    "dealer": "Chery Antigua",
    "showroom": ["Chery Showroom", "CMS Auto Complex", "Scott's Hill Road, St. John's, Antigua"],
    "address": "Chery Showroom, CMS Auto Complex, Scott's Hill Road, St. John's, Antigua",
    "email": "sales@chery.ag",
    "domain": "chery.ag",
    "instagram": "https://www.instagram.com/cheryantigua/",
    "facebook": "https://www.facebook.com/cheryantigua",
    "warranty": "7-Year / 200,000 km Warranty",
}

# The ownership promise (replaces the campaign offer strip on changan.ag).
# Figures match the official Chery Caribbean warranty programme.
OFFER = [
    {"big": "7 Years",  "lbl": "Vehicle warranty",  "desc": "7-year / 200,000 km manufacturer warranty on every new Chery."},
    {"big": "10 Years", "lbl": "Engine warranty",   "desc": "10-year / 1,000,000 km coverage on the engine."},
    {"big": "1,000 km", "lbl": "First service",     "desc": "Complimentary first inspection at 1,000 km or 1 month."},
]

# ─────────────────────────────────────────────────────────────── model data
# NOTE: specs are indicative and carry a "confirm with dealer" disclaimer on
# every model page. Update any value to match your exact local trim.
MODELS = [
    {
        "slug": "tiggo-4",
        "seo_type": "1.5T Compact SUV",
        "seo_desc": "Chery Tiggo 4 in Antigua — a turbocharged 1.5T compact SUV with dual 10.25\" displays and full driver assistance. Book a test drive in St John's.",
        "name": "Tiggo 4",
        "type": "Compact SUV",
        "tagline": "Cross wonderful life.",
        "image": "images/tiggo-4.jpg",
        "hero": "images/tiggo-4-hero.jpg",
        "gallery": ["images/tiggo-4-g1.jpg", "images/tiggo-4-g2.jpg", "images/tiggo-4-g3.jpg",
                    "images/tiggo-4-g4.jpg", "images/tiggo-4-g5.jpg", "images/tiggo-4-g6.jpg"],
        "interior": ["images/tiggo-4-int1.jpg", "images/tiggo-4-int2.jpg", "images/tiggo-4-int3.jpg", "images/tiggo-4-int4.jpg"],
        "blurb": "With a turbocharged 1.5T engine, dual 10.25\" displays and a full suite of driver assistance, the Chery Tiggo 4 packs big-SUV equipment into an easy, island-sized package.",
        "lede": "The compact SUV that gives you more of everything. The Chery Tiggo 4 pairs a punchy 1.5T engine and smooth CVT with dual 10.25\" displays, wireless Apple CarPlay & Android Auto, and safety tech usually reserved for far bigger price tags.",
        "feature_offer": True,
        "specs": [
            ("Engine", "1.5T", "turbo petrol"),
            ("Power", "145 hp", "210 Nm"),
            ("Transmission", "CVT", "automatic"),
            ("Displays", "2×10.25\"", "cluster + touch"),
        ],
        "features": [
            "Turbocharged 1.5T engine with CVT",
            "Dual 10.25\" HD displays",
            "Wireless Apple CarPlay & Android Auto",
            "ADAS suite — AEB, adaptive cruise, blind-spot",
            "360° HD panoramic camera",
            "AC-ventilated front seats · 6-way power driver's seat",
            "Sunroof, ambient lighting & remote engine start",
            "50W wireless phone charging",
        ],
        "cockpit": [
            ("10.25\"", "Instrument cluster"),
            ("10.25\"", "HD touchscreen"),
            ("360°", "HD camera"),
            ("50W", "Wireless charging"),
        ],
        "perf": [("145", "hp", "Maximum power"), ("210", "N·m", "Maximum torque")],
        "perf_line": "1.5 TURBO · CVT",
        # (display name, chip thumb, 360 spin folder under images/360/<slug>/ or None)
        "spin_frames": 36,
        "colours": [
            ("Khaki White Pearl", "images/colours/tiggo-4-khaki-white-pearl.jpg", "khaki-white-pearl"),
            ("Moonlight Silver", "images/colours/tiggo-4-moonlight-silver.jpg", "moonlight-silver"),
            ("Bloodstone Red", "images/colours/tiggo-4-bloodstone-red.jpg", "bloodstone-red"),
            ("Carbon Black", "images/colours/tiggo-4-carbon-black.jpg", "carbon-black"),
            ("Phantom Gray", "images/colours/tiggo-4-phantom-gray.jpg", "phantom-gray"),
        ],
    },
    {
        "slug": "tiggo-4-hev",
        "seo_type": "Hybrid Compact SUV",
        "seo_desc": "Chery Tiggo 4 HEV in Antigua — CSH self-charging full hybrid, smooth in town and far lighter on fuel, no plug needed. Book a test drive today.",
        "name": "Tiggo 4 HEV",
        "type": "Compact Hybrid SUV",
        "tagline": "Cross wonderful life — electrified.",
        "image": "images/tiggo-4-hev.jpg",
        "hero": "images/tiggo-4-hev-hero.jpg",
        "gallery": ["images/tiggo-4-hev-g1.jpg", "images/tiggo-4-hev-g2.jpg", "images/tiggo-4-hev-g3.jpg",
                    "images/tiggo-4-hev-g4.jpg", "images/tiggo-4-hev-g5.jpg", "images/tiggo-4-hev-g6.jpg"],
        "interior": ["images/tiggo-4-hev-int2.jpg", "images/tiggo-4-hev-int1.jpg", "images/tiggo-4-hev-int3.jpg", "images/tiggo-4-hev-int4.jpg"],
        "blurb": "The Tiggo 4 you know, with Chery's CSH full-hybrid drive — self-charging, whisper-smooth in town and dramatically lighter on fuel, with no plug required.",
        "lede": "All the equipment of the Tiggo 4, powered by Chery's CSH full-hybrid system. A 1.5L engine and DHT electric drive work together seamlessly — instant, quiet response in town, big fuel savings on every drive, and it charges itself as you go. No plug, no compromise.",
        "feature_offer": False,
        "specs": [
            ("Powertrain", "Hybrid", "1.5L + DHT"),
            ("System output", "≈204 hp", "combined"),
            ("Transmission", "e-CVT", "DHT"),
            ("Charging", "Self", "no plug needed"),
        ],
        "features": [
            "CSH full-hybrid — self-charging, no plug",
            "1.5L engine + DHT electric drive",
            "Whisper-quiet electric running in town",
            "Dramatically lower fuel consumption",
            "Dual 10.25\" HD displays",
            "Wireless Apple CarPlay & Android Auto",
            "ADAS suite — AEB, adaptive cruise, blind-spot",
            "Full LED lighting & keyless entry",
        ],
        "cockpit": [
            ("10.25\"", "Instrument cluster"),
            ("10.25\"", "HD touchscreen"),
            ("EV", "Quiet town driving"),
            ("Hybrid", "Self-charging"),
        ],
        "perf": [("204", "hp", "System output"), ("310", "N·m", "Combined torque")],
        "perf_line": "1.5L HYBRID · DHT",
        # shares the Tiggo 4 spin sets (same body)
        "spin_frames": 36,
        "spin_dir": "tiggo-4",
        "colours": [
            ("Khaki White Pearl", "images/colours/tiggo-4-khaki-white-pearl.jpg", "khaki-white-pearl"),
            ("Moonlight Silver", "images/colours/tiggo-4-moonlight-silver.jpg", "moonlight-silver"),
            ("Bloodstone Red", "images/colours/tiggo-4-bloodstone-red.jpg", "bloodstone-red"),
            ("Carbon Black", "images/colours/tiggo-4-carbon-black.jpg", "carbon-black"),
            ("Phantom Gray", "images/colours/tiggo-4-phantom-gray.jpg", "phantom-gray"),
        ],
    },
    {
        "slug": "tiggo-7-pro",
        "seo_type": "1.6T Mid-size SUV",
        "seo_desc": "Chery Tiggo 7 Pro in Antigua — a 194 hp 1.6T mid-size SUV with 7-speed dual-clutch and dual 12.3\" displays. Book a test drive in St John's.",
        "name": "Tiggo 7 Pro",
        "type": "Mid-size SUV",
        "tagline": "All the way with you.",
        "image": "images/tiggo-7.jpg",
        "hero": "images/tiggo-7-hero.jpg",
        "gallery": ["images/tiggo-7-g1.jpg", "images/tiggo-7-g2.jpg", "images/tiggo-7-g3.jpg",
                    "images/tiggo-7-g4.jpg", "images/tiggo-7-g5.jpg", "images/tiggo-7-g6.jpg"],
        "interior": ["images/tiggo-7-int0.jpg", "images/tiggo-7-int1.jpg", "images/tiggo-7-int2.jpg", "images/tiggo-7-int3.jpg"],
        "blurb": "With a 194 hp 1.6T engine, 7-speed dual-clutch and dual 12.3\" displays, the Chery Tiggo 7 Pro brings genuine refinement to the everyday island drive.",
        "lede": "Sleek design outside, serious refinement inside. The Chery Tiggo 7 Pro pairs a responsive 1.6T turbo with a 7-speed dual-clutch, dual 12.3\" displays and ventilated seats — the mid-size SUV that feels a class above.",
        "feature_offer": False,
        "specs": [
            ("Engine", "1.6T", "turbo petrol"),
            ("Power", "194 hp", "290 Nm"),
            ("Transmission", "7DCT", "dual-clutch"),
            ("Displays", "2×12.3\"", "cluster + touch"),
        ],
        "features": [
            "1.6T turbo — 194 hp / 290 Nm",
            "7-speed dual-clutch transmission",
            "Dual 12.3\" HD displays",
            "AC-ventilated front seats · leather appointed",
            "360° HD cameras with 3D view",
            "Panoramic sunroof with electric sunshade",
            "Induction-powered tailgate & N95 cabin filter",
            "Wireless Apple CarPlay & Android Auto",
        ],
        "cockpit": [
            ("12.3\"", "Instrument cluster"),
            ("12.3\"", "HD touchscreen"),
            ("360° 3D", "HD cameras"),
            ("50W", "Wireless charging"),
        ],
        "perf": [("194", "hp", "Maximum power"), ("290", "N·m", "Maximum torque")],
        "perf_line": "1.6 TURBO · 7DCT",
        "spin_frames": 36,
        "colours": [
            ("Khaki Pearl White", "images/colours/tiggo-7-khaki-pearl-white.jpg", "khaki-pearl-white"),
            ("White · Black Roof", "images/colours/tiggo-7-khaki-pearl-white-black-roof.jpg", "khaki-pearl-white-black-roof"),
            ("Bloodstone Red", "images/colours/tiggo-7-bloodstone-red.jpg", "bloodstone-red"),
            ("Carbon Black", "images/colours/tiggo-7-carbon-black.jpg", "carbon-black"),
            ("Phantom Gray", "images/colours/tiggo-7-phantom-gray.jpg", "phantom-gray"),
            ("Nasdaq Silver", "images/colours/tiggo-7-phantom-gray-black-roof.jpg", "phantom-gray-black-roof"),
        ],
    },
    {
        "slug": "tiggo-8",
        "seo_type": "7-Seat SUV",
        "seo_desc": "Chery Tiggo 8 in Antigua — a seven-seat SUV with up to 254 hp, ZF all-wheel drive and a 15.6\" smart cockpit. Book a test drive in St John's.",
        "name": "Tiggo 8",
        "type": "7-Seat SUV",
        "tagline": "Enjoy your first class.",
        "image": "images/tiggo-8.jpg",
        "hero": "images/tiggo-8-hero.jpg",
        "gallery": ["images/tiggo-8-g4.jpg", "images/tiggo-8-g5.jpg", "images/tiggo-8-g6.jpg",
                    "images/tiggo-8-g1.jpg", "images/tiggo-8-g2.jpg", "images/tiggo-8-g3.jpg"],
        "interior": ["images/tiggo-8-int0.jpg", "images/tiggo-8-int1.jpg", "images/tiggo-8-int2.jpg", "images/tiggo-8-int3.jpg"],
        "blurb": "With three rows of genuine space, up to 254 hp with ZF all-wheel drive, and a 15.6\" smart cockpit, the new Chery Tiggo 8 is first-class travel for all seven seats.",
        "lede": "Seven seats, zero compromise. The all-new Chery Tiggo 8 pairs turbo power — up to a 254 hp 2.0T with ZF intelligent AWD — with a frosted-leather cabin, a 15.6\" Snapdragon-powered smart screen and comfort engineered for every row.",
        "feature_offer": False,
        "specs": [
            ("Seats", "7", "2 + 3 + 2"),
            ("Engine", "1.6T / 2.0T", "turbo petrol"),
            ("Power", "up to 254 hp", "390 Nm"),
            ("Transmission", "7DCT", "2WD / AWD"),
        ],
        "features": [
            "Three rows — first-class comfort for 7",
            "1.6T 197 hp or 2.0T 254 hp with ZF AWD",
            "15.6\" smart screen · Snapdragon 8155",
            "12-speaker Sony premium sound (Premium)",
            "540° HD surround cameras",
            "Frosted leather · heated & ventilated seats",
            "Panoramic sunroof & AR head-up display",
            "Intelligent powered tailgate",
        ],
        "cockpit": [
            ("15.6\"", "Smart screen"),
            ("12", "Sony speakers"),
            ("540°", "HD cameras"),
            ("AR", "Head-up display"),
        ],
        "perf": [("254", "hp", "Maximum power"), ("390", "N·m", "Maximum torque")],
        "perf_line": "2.0 TURBO · AWD · 7DCT",
        "spin_frames": 24,
        "colours": [
            ("Khaki White Pearl", "images/colours/tiggo-8-khaki-white-pearl.jpg", "khaki-white-pearl"),
            ("Carbon Black", "images/colours/tiggo-8-carbon-black.jpg", "carbon-black"),
            ("Bamboo Gray", "images/colours/tiggo-8-bamboo-gray.jpg", "bamboo-gray"),
            ("Aurora Green", "images/colours/tiggo-8-aurora-green.jpg", "aurora-green"),
        ],
    },
    {
        "slug": "tiggo-9",
        "seo_type": "Flagship 7-Seat SUV",
        "seo_desc": "Chery Tiggo 9 in Antigua — the 241 hp 2.0T AWD flagship with Nappa leather, massage seats and 14 Sony speakers. Book a test drive in St John's.",
        "name": "Tiggo 9",
        "type": "Flagship 7-Seat SUV",
        "tagline": "One step ahead.",
        "image": "images/tiggo-9.jpg",
        "hero": "images/tiggo-9-hero.jpg",
        "gallery": ["images/tiggo-9-g1.jpg", "images/tiggo-9-g2.jpg", "images/tiggo-9-g3.jpg"],
        "interior": ["images/tiggo-9-int0.jpg", "images/tiggo-9-int1.jpg", "images/tiggo-9-int3.jpg", "images/tiggo-9-int4.jpg"],
        "blurb": "Nappa leather, massage seats, 14 Sony speakers and a 241 hp 2.0T with AWD — the Chery Tiggo 9 is the flagship that redefines what seven seats can feel like.",
        "lede": "The flagship. The Chery Tiggo 9 wraps seven seats in Nappa leather with massage and ventilation front seats, 14-speaker Sony sound and a 15.6\" smart cockpit — driven by a 241 hp 2.0T with all-wheel drive and 20\" alloys. One step ahead, in every direction.",
        "feature_offer": False,
        "specs": [
            ("Seats", "7", "flagship comfort"),
            ("Engine", "2.0T", "AWD"),
            ("Power", "241 hp", "390 Nm"),
            ("Wheels", "20\"", "alloy"),
        ],
        "features": [
            "Nappa leather · massage & ventilated front seats",
            "2.0T turbo — 241 hp / 390 Nm · AWD",
            "14-speaker Sony sound with headrest audio",
            "15.6\" smart screen · Snapdragon 8155",
            "540° HD surround cameras & VR head-up display",
            "10 wraparound safety airbags",
            "Full ADAS with autonomous valet parking",
            "Panoramic sunroof & rear window shades",
        ],
        "cockpit": [
            ("Nappa", "Massage seats"),
            ("14", "Sony speakers"),
            ("15.6\"", "Smart screen"),
            ("10", "Airbags"),
        ],
        "perf": [("241", "hp", "Maximum power"), ("390", "N·m", "Maximum torque")],
        "perf_line": "2.0 TURBO · AWD · 8AT",
        # no 360 set yet — a curated mosaic gallery instead of the colour picker.
        # (span classes: w2 = 2 columns, h2 = 2 rows)
        "lux_gallery": [
            ("images/tiggo-9-lux1.jpg",  "w2 h2", "Tiggo 9 in Antigua"),
            ("images/tiggo-9-lux5.jpg",  "w2",    "15.6\" smart cockpit"),
            ("images/tiggo-9-lux6.jpg",  "",      "Nappa front seats"),
            ("images/tiggo-9-lux4.jpg",  "",      "20\" alloy wheels"),
            ("images/tiggo-9-lux2.jpg",  "w2",    "Aurora Green"),
            ("images/tiggo-9-lux7.jpg",  "",      "Headrest speakers"),
            ("images/tiggo-9-lux8.jpg",  "",      "Flat-fold boot space"),
            ("images/tiggo-9-lux3.jpg",  "",      "Rear three-quarter"),
            ("images/tiggo-9-lux9.jpg",  "w2",    "Diamond grille"),
            ("images/tiggo-9-lux10.jpg", "",      "Top view"),
        ],
    },
]

DISCLAIMER = ("Features, specifications and colour options may vary by trim, model year and availability. "
              "Please confirm final specifications, availability and pricing with " + SITE["dealer"] + ".")

# ─────────────────────────────────────────── detailed brochure spec sheets
# Figures compiled from the official Chery Caribbean spec sheets (Fidelity
# Motors, Jamaica) and the factory RHD spec matrices — covered by DISCLAIMER.
TECH = {
    "tiggo-4": [
        ("Dimensions", [("Overall length", "4,330 mm"), ("Overall width", "1,830 mm"),
            ("Overall height", "1,662 mm"), ("Wheelbase", "2,610 mm"), ("Curb weight", "1,495 kg"),
            ("Boot capacity", "380–1,225 L"), ("Fuel tank", "51 L"), ("Seats", "5")]),
        ("Chassis & Performance", [("Engine (Comfort)", "1.5L · 111 hp / 138 Nm"),
            ("Engine (Premium)", "1.5 Turbo · 145 hp / 210 Nm"), ("Transmission", "CVT automatic"),
            ("Drivetrain", "Front-wheel drive"), ("Suspension", "Front independent · rear torsion beam"),
            ("Wheels (Comfort)", "16\" alloy"), ("Wheels (Premium)", "18\" alloy · red calipers"),
            ("Spare", "T-type"), ("Parking", "EPB electronic + Auto Hold")]),
        ("Safety & Driver Assistance", [("Airbags", "7 surround incl. centre & curtain"),
            ("ESP + ABS + EBD", "Standard"), ("Hill hold & descent", "Standard"),
            ("ACC", "Adaptive cruise (Premium)"), ("AEB / FCW", "Premium"),
            ("BSD / RCTA / LCA", "Premium"), ("LDW / IHBC", "Premium"),
            ("TPMS", "Standard"), ("Cameras", "Rear (Comfort) · 360° HD (Premium)")]),
        ("Exterior", [("Headlights", "Automatic LED"), ("DRL & tail lights", "LED"),
            ("Sunroof", "With sunshades (Premium)"), ("Mirrors", "Auto-folding · position memory (Premium)"),
            ("Wipers", "Rain-sensing (Premium)"), ("Windows", "One-touch power"),
            ("Entry", "Smart keyless · remote engine start")]),
        ("Infotainment & Interior", [("Instrument cluster", "10.25\" liquid crystal"),
            ("Touchscreen", "10.25\" HD"), ("Smartphone", "Wireless Apple CarPlay & Android Auto"),
            ("Voice control", "AI assistant"), ("Speakers", "6"),
            ("Wireless charging", "50W (Premium)"), ("Seats", "Leather · AC-ventilated front (Premium)"),
            ("Driver seat", "6-way power w/ lumbar (Premium)"), ("A/C", "Dual-zone (Premium)"),
            ("Ambient lighting", "Multi-colour (Premium)")]),
    ],
    "tiggo-4-hev": [
        ("Dimensions", [("Overall length", "≈ 4,330 mm"), ("Overall width", "≈ 1,830 mm"),
            ("Overall height", "≈ 1,662 mm"), ("Wheelbase", "≈ 2,610 mm"), ("Seats", "5")]),
        ("Hybrid Powertrain", [("System", "CSH full hybrid — self-charging"),
            ("Engine", "1.5L petrol"), ("Hybrid drive", "DHT150 e-CVT"),
            ("System output", "≈ 204 hp (150 kW)"), ("Combined torque", "≈ 310 Nm"),
            ("Charging", "Self-charging — no plug required"),
            ("Drivetrain", "Front-wheel drive")]),
        ("Safety & Driver Assistance", [("Airbags", "Front · side · curtain"),
            ("ESP + ABS + EBD", "Standard"), ("AEB / ACC", "Premium trim"),
            ("BSD / RCTA / DOW", "Premium trim"), ("MCB", "Multi-collision brake"),
            ("TPMS", "Standard"), ("Camera", "Rear · 360° HD (Premium)")]),
        ("Exterior", [("Headlights", "Automatic LED"), ("DRL & tail lights", "LED"),
            ("Mirrors", "Power fold · heated · indicators"), ("Windows", "One-touch power"),
            ("Entry", "Smart keyless · push-button start")]),
        ("Infotainment & Interior", [("Instrument cluster", "10.25\" digital"),
            ("Touchscreen", "10.25\" HD"), ("Smartphone", "Wireless Apple CarPlay & Android Auto"),
            ("Speakers", "up to 6"), ("Wireless charging", "15W (Premium)"),
            ("A/C", "Dual-zone automatic"), ("Seats", "Faux leather · heated front (Premium)")]),
    ],
    "tiggo-7-pro": [
        ("Dimensions", [("Overall length", "4,553 mm"), ("Overall width", "1,862 mm"),
            ("Overall height", "1,696 mm"), ("Wheelbase", "2,670 mm"), ("Curb weight", "1,518–1,603 kg"),
            ("Boot capacity", "475–1,500 L"), ("Fuel tank", "51 L"), ("Seats", "5")]),
        ("Chassis & Performance", [("Engine (Comfort)", "1.5 Turbo · 145 hp / 210 Nm · 6DCT"),
            ("Engine (LUX)", "1.6 Turbo · 194 hp / 290 Nm · 7DCT"),
            ("Drivetrain", "Front-wheel drive"), ("Rear suspension", "Independent"),
            ("Steering", "Electric power steering (EPS)"),
            ("Wheels (Comfort)", "18\" gloss black alloy"), ("Wheels (LUX)", "19\" glossy alloy"),
            ("Parking", "EPB electronic + Auto Hold")]),
        ("Safety & Driver Assistance", [("Airbags", "Up to 7 incl. knee & curtain (LUX)"),
            ("ESP + ABS + EBD", "Standard"), ("Driver monitoring", "LUX"),
            ("BSD / RCTA / RCTB", "LUX"), ("DOW / RCW", "LUX"),
            ("Cruise control", "Standard"), ("TPMS", "Standard"),
            ("Cameras", "Rear (Comfort) · 360° 3D HD (LUX)")]),
        ("Exterior", [("Headlights", "Automatic LED"), ("Tailgate", "Induction powered"),
            ("Sunroof", "Panoramic w/ electric sunshade (LUX)"), ("Mirrors", "Auto-folding"),
            ("Wipers", "Rain-sensing (LUX)"), ("Exhaust", "Double pipes (LUX)"),
            ("Entry", "Smart keyless · remote engine start (LUX)")]),
        ("Infotainment & Interior", [("Instrument cluster", "12.3\" liquid crystal"),
            ("Touchscreen", "12.3\" HD · Snapdragon 8155 w/ nav (LUX)"),
            ("Smartphone", "Wireless Apple CarPlay & Android Auto"), ("Speakers", "6"),
            ("Wireless charging", "50W (LUX)"), ("Seats", "AC-ventilated front · leather (LUX)"),
            ("A/C", "Dual-zone w/ second-row vents · N95 filter"),
            ("Ambient lighting", "Multi-colour")]),
    ],
    "tiggo-8": [
        ("Dimensions", [("Overall length", "4,725 mm"), ("Overall width", "1,860 mm"),
            ("Overall height", "1,705 mm"), ("Wheelbase", "2,710 mm"), ("Curb weight", "1,789 kg"),
            ("Boot capacity", "193–1,930 L"), ("Fuel tank", "57 L"), ("Seats", "7 (2+3+2)")]),
        ("Chassis & Performance", [("Engine (2WD Comfort)", "1.6 Turbo · 197 hp / 290 Nm"),
            ("Engine (4WD Premium)", "2.0 Turbo · 254 hp / 390 Nm"),
            ("Transmission", "7-speed dual-clutch (7DCT)"),
            ("Drivetrain", "2WD · ZF intelligent AWD (Premium)"),
            ("Wheels", "18\" (Comfort) · 19\" (Premium)"), ("Spare", "T-type"),
            ("Parking", "EPB electronic + Auto Hold")]),
        ("Safety & Driver Assistance", [("Airbags", "Up to 8 incl. knee & 2nd-row side"),
            ("ESP + ABS + EBD", "Standard"), ("ACC / ICA / TJA", "Premium"),
            ("AEB / FCW / LDW", "Premium"), ("ELKA / IHBC", "Premium"),
            ("BSD / DOW / RCTA", "Premium"), ("TPMS", "Standard"),
            ("Cameras", "Reverse w/ sensors · 540° HD surround (Premium)")]),
        ("Exterior", [("Headlights", "Automatic LED"), ("Tailgate", "Powered · intelligent (Premium)"),
            ("Sunroof", "Panoramic w/ electric sunshades (Premium)"),
            ("Mirrors", "Power fold · heated"), ("Wipers", "Rain-sensing"),
            ("Entry", "Smart keyless · remote engine start")]),
        ("Infotainment & Interior", [("Touchscreen", "15.6\" · Qualcomm Snapdragon 8155"),
            ("Instrument cluster", "10.25\" liquid crystal"), ("Head-up display", "AR reality"),
            ("Smartphone", "Wireless Apple CarPlay & Android Auto"),
            ("Sound", "8 speakers · 12-speaker Sony (Premium)"), ("Wireless charging", "50W"),
            ("Seats", "Frosted leather · ventilated & heated (Premium)"),
            ("A/C", "Two-zone auto · AQS ion purification (Premium)"),
            ("Ambient lighting", "Multi-colour")]),
    ],
    "tiggo-9": [
        ("Dimensions", [("Overall length", "4,810 mm"), ("Overall width", "1,925 mm"),
            ("Overall height", "1,741 mm"), ("Wheelbase", "2,800 mm"), ("Curb weight", "1,899 kg"),
            ("Boot capacity", "717–2,021 L"), ("Fuel tank", "65 L"), ("Seats", "7")]),
        ("Chassis & Performance", [("Engine", "2.0 Turbo · 241 hp / 390 Nm"),
            ("Transmission", "8-speed automatic (8AT)"), ("Drivetrain", "All-wheel drive"),
            ("Suspension", "Front & rear independent"), ("Steering", "Electric power steering (EPS)"),
            ("Wheels", "20\" alloy · branded tyres"), ("Parking", "EPB electronic + Auto Hold")]),
        ("Safety & Driver Assistance", [("Airbags", "10 wraparound incl. far-side centre"),
            ("ESP + ABS + EBD", "Standard"), ("ACC / ICA / TJA", "Standard"),
            ("AEB / FCW / LDW / LDP", "Standard"), ("ELKA / IHBC / DMS", "Standard"),
            ("BSD / DOW / LCA / RCTA / RCW", "Standard"),
            ("Valet parking", "Autonomous (APA)"), ("TPMS", "Standard"),
            ("Cameras", "540° HD surround")]),
        ("Exterior", [("Headlights", "Automatic LED"), ("Tailgate", "Intelligent electric powered"),
            ("Sunroof", "Panoramic w/ electric sunshades"), ("Rear windows", "Pull-up shades"),
            ("Mirrors", "Auto-folding · position memory"), ("Wipers", "Rain-sensing"),
            ("Entry", "Smart keyless · remote engine start")]),
        ("Infotainment & Interior", [("Touchscreen", "15.6\" · Qualcomm Snapdragon 8155"),
            ("Instrument cluster", "10.25\" liquid crystal"), ("Head-up display", "Virtual reality"),
            ("Sound", "14-speaker Sony · driver headrest audio"),
            ("Smartphone", "Wireless Apple CarPlay & Android Auto"), ("Wireless charging", "50W"),
            ("Seats", "Nappa leather · massage, ventilation & heating"),
            ("Front passenger", "One-click comfortable lying w/ legrest"),
            ("A/C", "Dual-zone · PM2.5 filtration"), ("Armrest", "Cooled")]),
    ],
}

# ───────────────────────────────────────────────────────────── svg + icons
def logo(prefix, dark=False):
    # Official Chery lockup (emblem + wordmark). Dark version for light UI.
    src = "chery-logo.png" if dark else "chery-logo-white.png"
    return f'<img class="mark" src="{prefix}images/{src}" alt="Chery" width="92" height="38">'

IC_SHIELD = '<svg viewBox="0 0 24 24" width="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 3v6c0 5-3.4 8.5-8 11-4.6-2.5-8-6-8-11V5l8-3z"/></svg>'
IC_WRENCH = '<svg viewBox="0 0 24 24" width="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2-2 2.5-2.5z"/></svg>'
IC_PEOPLE = '<svg viewBox="0 0 24 24" width="22" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5.5a3 3 0 0 1 0 5.5M18 20c0-2.4-1-4.5-2.5-5.7"/></svg>'
IC_WA = '<svg viewBox="0 0 448 512" width="30" height="30" fill="currentColor" aria-hidden="true"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>'
IC_MENU = '<svg viewBox="0 0 24 24" width="26" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg>'
# Steering wheel — the Test Drive nav icon (label appears on hover)
IC_WHEEL = '<svg viewBox="0 0 24 24" width="22" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9.2"/><circle cx="12" cy="12" r="2.7"/><path d="M12 14.7V21M9.7 11.1 4.2 8.4M14.3 11.1l5.5-2.7"/></svg>'
IC_TICK = '<svg class="tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"/></svg>'
IC_WA_SM = '<svg class="wa-sm" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.1-.7.2-.2.3-.7 1-.9 1.1-.2.2-.3.2-.6.1-1.6-.8-2.6-1.4-3.7-3.2-.3-.5.3-.5.8-1.5.1-.2 0-.4 0-.5 0-.2-.7-1.6-.9-2.2-.2-.6-.5-.5-.7-.5H8c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.3 5.2 4.6 1.9.8 2.7.9 3.6.8.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15l-1.3 4.7 4.8-1.3A10 10 0 1 0 12 2z"/></svg>'
IC_CARET = '<svg class="caret" viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
IC_ARW = '<svg class="arw" viewBox="0 0 24 24" width="17" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
IC_IG = '<svg viewBox="0 0 24 24" width="20" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
IC_FB = '<svg viewBox="0 0 24 24" width="20" fill="currentColor"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H7v3h3v6h3v-6h3l1-3h-4v-2c0-.6.4-1 1-1z"/></svg>'

E = html.escape

# ───────────────────────────────────────────────────────── shared partials
# ══════════════════════════════════════════════════ SEO, analytics & security
# Everything below is generated output plumbing — canonical URLs, Open Graph /
# Twitter cards, JSON-LD structured data, the GA4 tag, sitemap.xml, robots.txt
# and the security headers. Page copy (titles / descriptions) lives with each
# page; the per-model "seo_title" and "seo_desc" fields live in MODELS above.

BASE_URL  = "https://chery.ag"        # canonical origin — no trailing slash
SITE_NAME = "Chery Antigua"             # og:site_name / JSON-LD dealer name
BRAND     = "Chery"           # brand as it reads in copy & schema
LOCALE    = "en_GB"
THEME     = "#131619"                 # browser UI colour (matches the header)

# Origin of the VMP `ingestWebLead` endpoint the forms post to (assets/site.js).
# Named here so the Content-Security-Policy connect-src stays in step with it.
LEAD_ORIGIN = "https://wqlvyeuqaejbtsrlbpvt.supabase.co"

# ── Google Analytics 4 ──────────────────────────────────────────────────────
# Paste the GA4 Measurement ID (looks like G-XXXXXXXXXX) between the quotes and
# re-run `python3 build.py`. While it is empty NO analytics tag is emitted, no
# Google script is loaded and no cookies are set — the site ships clean until
# the property is ready. The tag is loaded from an external analytics.js (also
# generated here) so the pages carry no inline JavaScript and the strict
# Content-Security-Policy in _headers needs no 'unsafe-inline' for scripts.
GA4_ID = "G-WE9Y3926QN"

def canonical(path):
    """Absolute URL for a site-relative page path.

    '' / 'index.html' → the site root, and any directory index (models/index.html)
    → the directory URL, so there is exactly one canonical form per page.
    """
    if path in ("", "index.html"):
        return BASE_URL + "/"
    if path.endswith("/index.html"):
        return BASE_URL + "/" + path[: -len("index.html")]
    return BASE_URL + "/" + path

def abs_url(rel):
    """Absolute URL for a site-relative asset path."""
    return BASE_URL + "/" + str(rel).lstrip("/")

def analytics(prefix):
    """GA4 loader — two external scripts, no inline JS. Empty when GA4_ID is."""
    if not GA4_ID:
        return ""
    return (f'\n  <link rel="preconnect" href="https://www.googletagmanager.com">'
            f'\n  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>'
            f'\n  <script src="{prefix}assets/analytics.js"></script>')

# ─────────────────────────────────────────────────────────── structured data
def ld(*objects):
    """Render one or more JSON-LD objects as <script> blocks for the <head>."""
    out = ""
    for obj in objects:
        if not obj:
            continue
        txt = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        txt = txt.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
        out += f'\n  <script type="application/ld+json">{txt}</script>'
    return out

def dealer_ld():
    """The dealership itself — referenced by @id from every other block."""
    d = {
        "@type": "AutoDealer",
        "@id": BASE_URL + "/#dealer",
        "name": SITE_NAME,
        "legalName": SITE["dealer"],
        "url": BASE_URL + "/",
        "image": abs_url(HERO_IMAGE),
        "email": SITE["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "CMS Auto Complex, Scott's Hill Road",
            "addressLocality": "St John's",
            "addressCountry": "AG",
        },
        "areaServed": {"@type": "Country", "name": "Antigua and Barbuda"},
        "brand": {"@type": "Brand", "name": BRAND},
        "sameAs": [u for u in (SITE.get("instagram"), SITE.get("facebook")) if u],
    }
    tel = SITE.get("phone") or SITE.get("whatsapp")
    if tel:
        d["telephone"] = tel
    return d

def website_ld():
    return {
        "@type": "WebSite",
        "@id": BASE_URL + "/#website",
        "url": BASE_URL + "/",
        "name": SITE_NAME,
        "inLanguage": "en",
        "publisher": {"@id": BASE_URL + "/#dealer"},
    }

def breadcrumb_ld(trail):
    """trail = [(name, absolute-url), …] in order from the home page down."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": u}
            for i, (n, u) in enumerate(trail, start=1)
        ],
    }

def fuel_type(type_line):
    """Map a model's display type to a schema.org fuelType value."""
    t = type_line.lower()
    if "plug-in" in t or "erev" in t or "dm-i" in t:
        return "Plug-in Hybrid Electric"
    if "hybrid" in t or "hev" in t:
        return "Hybrid Electric"
    if "electric" in t:
        return "Electric"
    if "diesel" in t:
        return "Diesel"
    return "Gasoline"

def vehicle_ld(m):
    url = canonical(f"models/{m['slug']}.html")
    images = [abs_url(i) for i in (m.get("hero"), m.get("image")) if i]
    return {
        "@context": "https://schema.org",
        "@type": "Vehicle",
        "@id": url + "#vehicle",
        "name": f"{BRAND} {m['name']}",
        "url": url,
        "description": m["seo_desc"],
        "image": images,
        "brand": {"@type": "Brand", "name": BRAND},
        "manufacturer": {"@type": "Organization", "name": BRAND},
        "model": m["name"],
        "bodyType": m["type"].split("·")[0].strip(),
        "vehicleConfiguration": m["type"].replace("·", "—"),
        "fuelType": fuel_type(m["type"]),
        "offers": {
            "@type": "Offer",
            "url": url,
            "availability": "https://schema.org/InStock",
            "areaServed": {"@type": "Country", "name": "Antigua and Barbuda"},
            "seller": {"@id": BASE_URL + "/#dealer"},
        },
    }

def home_ld():
    return {
        "@context": "https://schema.org",
        "@graph": [
            dealer_ld(),
            website_ld(),
            {
                "@type": "ItemList",
                "name": f"{BRAND} models available in Antigua & Barbuda",
                "itemListElement": [
                    {"@type": "ListItem", "position": i,
                     "name": f"{BRAND} {m['name']}",
                     "url": canonical(f"models/{m['slug']}.html")}
                    for i, m in enumerate(MODELS, start=1)
                ],
            },
        ],
    }

def contact_ld():
    return {
        "@context": "https://schema.org",
        "@graph": [
            dealer_ld(),
            {
                "@type": "ContactPage",
                "@id": canonical("contact.html") + "#page",
                "url": canonical("contact.html"),
                "name": f"Contact {SITE_NAME}",
                "inLanguage": "en",
                "about": {"@id": BASE_URL + "/#dealer"},
            },
        ],
    }


# ────────────────────────────────────────────────────── models index page
def build_models_index():
    """A real /models/ page: a category page search can rank, a proper
    breadcrumb target, and an internal-linking hub to every model."""
    p = "../"
    cards = "".join(
        f'<a class="mcard reveal" href="/models/{m["slug"]}.html">'
        f'<span class="ph"><img src="{p}{m["image"]}" alt="{BRAND} {E(m["name"])}" loading="lazy"></span>'
        f'<span class="tx"><h2 class="nm">{BRAND} {E(m["name"])}</h2>'
        f'<span class="ty">{E(m["type"])}</span>'
        f'<span class="bl">{E(m["blurb"])}</span></span></a>'
        for m in MODELS)

    body = f"""
{header(p)}

<main class="models-page">
  <div class="wrap">
    <div class="mp-head reveal in">
      <div class="overline">The range</div>
      <h1>{BRAND} models in Antigua &amp; Barbuda</h1>
      <p class="mp-lede">Every {BRAND} we sell on the island, with specifications,
      photography and a test drive you can book in a couple of taps. Sold and
      serviced by {SITE_NAME} — {SITE['address']}.</p>
    </div>
    <div class="mgrid">{cards}</div>
  </div>
</main>

{footer(p)}
{floating()}
{modal()}
{scripts(p)}"""

    title = f"All {BRAND} Models in Antigua | {SITE_NAME}"
    desc = (f"Every {BRAND} model available in Antigua & Barbuda — "
            + ", ".join(m["name"] for m in MODELS[:4])
            + f" and more. Specs, photos and test drives from {SITE_NAME}.")[:158]
    crumbs = breadcrumb_ld([("Home", BASE_URL + "/"),
                            ("Models", canonical("models/index.html"))])
    listing = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": canonical("models/index.html") + "#page",
        "url": canonical("models/index.html"),
        "name": f"{BRAND} models",
        "inLanguage": "en",
        "about": {"@id": BASE_URL + "/#dealer"},
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": f"{BRAND} {m['name']}",
                 "url": canonical(f"models/{m['slug']}.html")}
                for i, m in enumerate(MODELS, start=1)
            ],
        },
    }
    (ROOT / "models" / "index.html").write_text(
        head(title, desc, p, "models/index.html", jsonld=ld(listing, crumbs)) + body,
        encoding="utf-8")
    print("wrote models/index.html")

# ───────────────────────────────────────────────────────────── 404 page
def build_404():
    """Netlify serves this for any unmatched path, at any depth — so every
    asset and link here must be root-absolute, not relative."""
    p = "/"
    body = f"""
{header(p)}

<main class="models-page">
  <div class="wrap" style="text-align:center">
    <div class="mp-head reveal in">
      <div class="overline center">Error 404</div>
      <h1>We can't find that page</h1>
      <p class="mp-lede" style="margin-inline:auto">The link may be out of date, or the
      page may have moved. The whole {BRAND} range is a click away — or talk to us and
      we'll point you in the right direction.</p>
      <h2 class="sr-only">Where to go next</h2>
      <div class="hero-cta" style="justify-content:center;margin-top:28px">
        <a class="btn btn-primary btn-lg" href="/models/">Browse the range</a>
        <a class="btn btn-outline btn-lg" href="/contact.html">Contact us</a>
      </div>
    </div>
  </div>
</main>

{footer(p)}
{floating()}
{modal()}
{scripts(p)}"""

    (ROOT / "404.html").write_text(
        head(f"Page not found | {SITE_NAME}",
             f"That page doesn't exist. Browse the full {BRAND} range in Antigua "
             f"or get in touch with {SITE_NAME}.",
             p, "404.html", robots="noindex, follow") + body,
        encoding="utf-8")
    print("wrote 404.html")

# ───────────────────────────────────────────── sitemap / robots / security
SECURITY_CONTACT = SITE["email"]   # where to report a vulnerability

def build_seo_files():
    """Writes sitemap.xml, robots.txt, _headers, _redirects, security.txt and
    (when GA4_ID is set) assets/analytics.js."""
    today = datetime.date.today().isoformat()

    # ── sitemap.xml — home, contact and every model page. Brochures are print
    #    duplicates of the model pages and are deliberately left out.
    pages = [("index.html", "1.0", "weekly"),
             ("models/index.html", "0.9", "weekly"),
             ("contact.html", "0.7", "monthly")]
    pages += [(f"models/{m['slug']}.html", "0.9", "monthly") for m in MODELS]
    entries = "".join(
        f"  <url>\n"
        f"    <loc>{canonical(path)}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{prio}</priority>\n"
        f"  </url>\n"
        for path, prio, freq in pages)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n", encoding="utf-8")

    # ── robots.txt
    (ROOT / "robots.txt").write_text(f"""# robots.txt — {SITE_NAME}
User-agent: *
Allow: /

# Print brochures duplicate the model pages — keep them out of the index,
# but let the downloadable PDFs be crawled.
Disallow: /brochures/
Allow: /brochures/pdf/

Sitemap: {BASE_URL}/sitemap.xml
""", encoding="utf-8")

    # ── _headers — Netlify / Cloudflare Pages security + caching headers.
    #    The CSP allowlist is deliberately tight: Google Fonts for type,
    #    googletagmanager/google-analytics for GA4, and the VMP lead endpoint
    #    for form posts. No 'unsafe-inline' for scripts — the pages carry no
    #    inline JavaScript at all.
    (ROOT / "_headers").write_text(f"""# Security & caching headers — Netlify / Cloudflare Pages.
# Generated by build.py. Edit the policy there, not here.

/*
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: accelerometer=(), autoplay=(), camera=(), display-capture=(), encrypted-media=(), fullscreen=(self), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), midi=(), payment=(), usb=(), xr-spatial-tracking=()
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-site
  X-DNS-Prefetch-Control: off
  Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'; manifest-src 'self'; img-src 'self' data: https://www.google-analytics.com https://www.googletagmanager.com; font-src 'self' https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; script-src 'self' https://www.googletagmanager.com; connect-src 'self' {LEAD_ORIGIN} https://www.google-analytics.com https://analytics.google.com https://region1.google-analytics.com https://www.googletagmanager.com; upgrade-insecure-requests

# Fingerprint-free asset paths change name rarely — revalidate daily.
/assets/*
  Cache-Control: public, max-age=86400, must-revalidate

/images/*
  Cache-Control: public, max-age=2592000, immutable

/brochures/pdf/*
  Cache-Control: public, max-age=2592000

# HTML must never be served stale — the build regenerates it.
/*.html
  Cache-Control: public, max-age=0, must-revalidate

/sitemap.xml
  Cache-Control: public, max-age=3600

/robots.txt
  Cache-Control: public, max-age=3600
""", encoding="utf-8")

    # ── _redirects — collapse /index.html onto the canonical root.
    (ROOT / "_redirects").write_text("""# Netlify / Cloudflare Pages redirects. Generated by build.py.
# Keep one canonical URL for the home page.
/index.html    /    301!
/models/index.html    /models/    301!
""", encoding="utf-8")

    # ── security.txt (RFC 9116). Expires one year from this build.
    wk = ROOT / ".well-known"
    wk.mkdir(exist_ok=True)
    expires = datetime.date.today().replace(year=datetime.date.today().year + 1)
    (wk / "security.txt").write_text(f"""# Vulnerability disclosure for {SITE['domain']} (RFC 9116)
Contact: mailto:{SECURITY_CONTACT}
Expires: {expires.isoformat()}T00:00:00.000Z
Preferred-Languages: en
Canonical: {BASE_URL}/.well-known/security.txt
""", encoding="utf-8")

    # ── assets/analytics.js — the GA4 bootstrap, kept out of the HTML so the
    #    CSP can forbid inline script. Removed again if the ID is cleared.
    ga_js = ROOT / "assets" / "analytics.js"
    if GA4_ID:
        ga_js.write_text(f"""/* GA4 bootstrap — GENERATED by build.py from GA4_ID. Do not edit by hand.
   Event tracking (leads, test drives, WhatsApp, calls) lives in site.js. */
window.dataLayer = window.dataLayer || [];
function gtag() {{ dataLayer.push(arguments); }}
gtag("js", new Date());
gtag("config", "{GA4_ID}");
""", encoding="utf-8")
        print(f"wrote assets/analytics.js (GA4 {GA4_ID})")
    elif ga_js.exists():
        ga_js.unlink()

    print("wrote sitemap.xml, robots.txt, _headers, _redirects, .well-known/security.txt")
    if not GA4_ID:
        print("  note: GA4_ID is empty — no analytics tag emitted. "
              "Set GA4_ID in build.py and re-run to switch it on.")


# ─────────────────────────────────────────── output post-processing (CWV)
_DIMS = {}

def _image_size(path):
    """Intrinsic pixel size of an image, or None if it can't be read."""
    if path not in _DIMS:
        try:
            from PIL import Image
            with Image.open(path) as im:
                _DIMS[path] = im.size
        except Exception:
            _DIMS[path] = None
    return _DIMS[path]

def add_image_dimensions():
    """Give every <img> its real width/height.

    The browser uses the ratio to reserve the right box before the bytes
    arrive, which is what keeps Cumulative Layout Shift at zero. Paired with
    `img { height: auto }` in the CSS, so nothing is visually resized — the
    object-fit rules on .hero-bg, .mband .media etc. are more specific and
    still win.

    Runs as a post-process over the written files so it covers every <img> the
    generator emits without threading sizes through each template.
    """
    added = 0
    pages = (list(ROOT.glob("*.html")) + list(ROOT.glob("models/*.html"))
             + list(ROOT.glob("brochures/*.html")))

    def fix(m):
        nonlocal added
        tag = m.group(0)
        if "width=" in tag or "height=" in tag:
            return tag
        src = re.search(r'src="([^"]+)"', tag)
        if not src or src.group(1).startswith(("http", "data:", "//")):
            return tag
        # every image lives under ROOT/images, whatever the page's depth
        # strip "../" (nested pages) and a leading "/" (the 404 page, which
        # must use root-absolute paths because it is served at any depth)
        rel = re.sub(r"^(\.\./)+", "", src.group(1)).lstrip("/")
        size = _image_size(ROOT / rel)
        if not size:
            return tag
        added += 1
        return tag[:-1].rstrip() + f' width="{size[0]}" height="{size[1]}">'

    for page in pages:
        html_text = page.read_text(encoding="utf-8")
        out = re.sub(r"<img\b[^>]*>", fix, html_text)
        if out != html_text:
            page.write_text(out, encoding="utf-8")
    print(f"added width/height to {added} images")

def head(title, desc, prefix, canonical_path, extra_head="", jsonld="",
         robots="index, follow", share_image=None, preload=None):
    """The <head> for every public page: title/description, canonical URL,
    Open Graph + Twitter cards, JSON-LD and the GA4 tag."""
    url   = canonical(canonical_path)
    share = abs_url(share_image or HERO_IMAGE)
    # Preloading the hero tells the browser to fetch the Largest Contentful
    # Paint image immediately, instead of waiting to discover it in the body.
    pre = (f'\n  <link rel="preload" as="image" href="{prefix}{preload}" fetchpriority="high">'
           if preload else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">{pre}
  <meta name="theme-color" content="{THEME}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{E(SITE_NAME)}">
  <meta property="og:locale" content="{LOCALE}">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:image" content="{share}">
  <meta property="og:image:alt" content="{E(title)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{E(title)}">
  <meta name="twitter:description" content="{E(desc)}">
  <meta name="twitter:image" content="{share}">
  <link rel="icon" type="image/png" href="{prefix}images/favicon.png">
  <link rel="apple-touch-icon" href="{prefix}images/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,600;1,700;1,800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/styles.css">{extra_head}{jsonld}{analytics(prefix)}
</head>
<body>"""

def header(prefix):
    mega = "".join(
        f'<a class="mega-item" href="/models/{m["slug"]}.html">'
        f'<span class="mega-thumb"><img src="{prefix}{m["image"]}" alt="Chery {E(m["name"])}" loading="lazy"></span>'
        f'<span class="mega-tx"><span class="mega-name">{E(m["name"])}</span>'
        f'<span class="mega-type">{E(m["type"])}</span></span></a>'
        for m in MODELS)
    return f"""
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="Chery Antigua home">
      {logo(prefix, dark=True)}
    </a>
    <nav class="nav-links">
      <div class="nav-item has-mega">
        <a class="link" href="/models/">Models {IC_CARET}</a>
        <div class="mega"><div class="mega-inner">{mega}</div></div>
      </div>
      <a class="link" href="/#promise">Warranty</a>
      <a class="link" href="/#why">Why Chery</a>
      <a class="link" href="/contact.html">Contact</a>
      <button class="btn btn-primary mobile-cta" data-quote data-model="">Request a Quote</button>
    </nav>
    <div class="nav-actions">
      <a class="nav-icon-btn" href="/contact.html" aria-label="Test Drive"><span class="ni-glyph">{IC_WHEEL}</span><span class="ni-label">Test Drive</span></a>
      <button class="hamburger" aria-label="Menu">{IC_MENU}</button>
      <button class="btn btn-primary btn-sm" data-quote data-model="">Request a Quote</button>
    </div>
  </div>
</header>"""

def floating():
    return f"""
<div class="floating">
  <a class="fab fab-wa" data-wa data-model="" target="_blank" rel="noopener" aria-label="WhatsApp us">{IC_WA}</a>
</div>"""

def model_options(selected=""):
    opts = ['<option value="" disabled{sel}>Select a model…</option>'.format(
        sel=" selected" if not selected else "")]
    for m in MODELS:
        s = " selected" if m["name"] == selected else ""
        opts.append(f'<option value="{E(m["name"])}"{s}>{E(m["name"])}</option>')
    opts.append('<option value="Not sure yet">Not sure yet</option>')
    return "".join(opts)

def modal(selected=""):
    return f"""
<div class="modal-overlay" id="quoteModal" aria-hidden="true">
  <div class="modal" role="dialog" aria-modal="true" aria-label="Request a quote">
    <button class="modal-close" aria-label="Close">&times;</button>
    <div class="modal-head">
      <div class="overline">No obligation · 30 seconds</div>
      <h3>Request Your Quote</h3>
      <p>Tell us how to reach you and a member of our team will call with your personalised quote.</p>
    </div>
    <form novalidate>
      <input class="hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
      <div class="row-2">
        <div class="field"><label>First name</label><input name="firstName" required autocomplete="given-name" placeholder="Jane"></div>
        <div class="field"><label>Last name</label><input name="lastName" autocomplete="family-name" placeholder="Doe"></div>
      </div>
      <div class="field"><label>Phone / WhatsApp</label><input name="phone" type="tel" required autocomplete="tel" placeholder="+1 (268) 464-3345"></div>
      <div class="field"><label>Email</label><input name="email" type="email" autocomplete="email" placeholder="you@email.com"></div>
      <div class="row-2">
        <div class="field"><label>I'd like to…</label><select name="interest">
          <option value="Request a quote" selected>Request a quote</option>
          <option value="Book a test drive">Book a test drive</option>
          <option value="General enquiry">General enquiry</option>
        </select></div>
        <div class="field"><label>Model of interest</label><select name="model" required>{model_options(selected)}</select></div>
      </div>
      <div class="field"><label>Message <span style="opacity:.6">(optional)</span></label><textarea name="message" placeholder="Any questions or preferences?"></textarea></div>
      <button class="btn btn-primary" type="submit">Send My Request →</button>
      <p class="form-fine">By submitting you agree to be contacted by {E(SITE['dealer'])}.</p>
    </form>
    <div class="thankyou">
      <div class="check">&#10003;</div>
      <h3>Thank you, <span data-thanks-name>there</span>!</h3>
      <p>We've received your request. A member of our team will contact you shortly with your personalised quote.</p>
    </div>
  </div>
</div>"""

HERO_IMAGE = "images/hero-tiggo7.jpg"  # home hero — red Tiggo 7 Pro, golden-hour coast road

def footer(prefix):
    model_links = "".join(
        f'<a href="/models/{m["slug"]}.html">{E(m["name"])}</a>' for m in MODELS)
    return f"""
<footer class="site-footer" id="contact">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="brand" href="/">{logo(prefix)}</a>
        <p class="foot-addr">{'<br>'.join(E(l) for l in SITE['showroom'])}</p>
        <div class="foot-contact">
          <a data-wa data-model="" target="_blank" rel="noopener">WhatsApp +1 (268) 464-3345</a>
          <a href="mailto:{SITE['email']}">{E(SITE['email'])}</a>
        </div>
      </div>
      <div>
        <h4>Models</h4>
        {model_links}
      </div>
      <div>
        <h4>Visit</h4>
        <a href="/contact.html">Contact &amp; Test Drive</a>
        <a href="/#promise">Warranty Promise</a>
        <a href="/#why">Why Buy From Us</a>
        <a data-quote data-model="" href="#">Request a Quote</a>
        <div class="socials" style="margin-top:14px">
          <a href="{SITE['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{IC_IG}</a>
          <a href="{SITE['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{IC_FB}</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 {E(SITE['brand'])} {E(SITE['sub'])}. All rights reserved.</span>
    </div>
  </div>
</footer>"""

def scripts(prefix, extra=""):
    return f'<script src="{prefix}assets/site.js"></script>{extra}\n</body>\n</html>'

# ─────────────────────────────────────────────────────────────── home page
def build_home():
    p = ""  # root prefix

    offer_items = "".join(
        f'<div class="offer-cell reveal"><div class="num">{E(o["big"])}</div>'
        f'<div class="lbl">{E(o["lbl"])}</div><div class="desc">{E(o["desc"])}</div></div>'
        for o in OFFER)

    bands = ""
    for i, m in enumerate(MODELS):
        rev = " rev" if i % 2 else ""
        mini = "".join(
            f'<div class="ms"><div class="v">{E(v)}{(" <small>"+E(s)+"</small>") if s else ""}</div>'
            f'<div class="k">{E(k)}</div></div>'
            for k, v, s in m["specs"][:3])
        bands += f"""
  <section class="mband{rev}" id="{m['slug']}">
    <div class="media"><img src="{p}{m['image']}" alt="Chery {E(m['name'])}" loading="lazy"></div>
    <div class="content">
      <div class="mtype reveal">{E(m['type'])}</div>
      <h2 class="reveal">{E(m['name'])}</h2>
      <div class="tagline reveal">{E(m['tagline'])}</div>
      <p class="blurb reveal">{E(m['blurb'])}</p>
      <div class="mini-specs reveal">{mini}</div>
      <div class="band-cta reveal">
        <button class="btn btn-primary" data-quote data-model="{E(m['name'])}">Request a Quote</button>
        <a class="btn-link" href="/models/{m['slug']}.html">Explore {E(m['name'])} {IC_ARW}</a>
      </div>
    </div>
  </section>"""

    why = [
        (IC_SHIELD, SITE["warranty"], "Backed by a 10-year / 1,000,000 km engine warranty — coverage you can count on."),
        (IC_WRENCH, "Genuine Parts & Servicing", "Factory-trained technicians and genuine Chery parts, right here on the island."),
        (IC_PEOPLE, "Dedicated Local Support", "A team ready to help — sales, service and everything after."),
    ]
    why_cards = "".join(
        f'<div class="why-card reveal"><div class="ic">{ic}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>'
        for ic, t, d in why)

    body = f"""
{header(p)}

<section class="hero">
  <div class="hero-bg"><img src="{p}{HERO_IMAGE}" alt="Chery Tiggo 7 Pro on the coast road" fetchpriority="high" decoding="async"></div>
  <div class="hero-inner wrap">
    <div class="overline reveal in">Chery · Antigua &amp; Barbuda</div>
    <h1 class="reveal in" style="margin-top:22px"><span class="sr-only">Chery Antigua — Tiggo SUVs and hybrids in St John's. </span>One step<br><span class="accent">ahead</span></h1>
    <p class="lede reveal in">The Tiggo family has arrived in Antigua — from the city-smart Tiggo 4 to the flagship Tiggo 9, with hybrid power in between. Premium cabins, full driver assistance and a 7-year warranty, backed by island-based sales and service.</p>
    <div class="hero-cta reveal in">
      <button class="btn btn-primary btn-lg" data-quote data-model="">Request a Quote</button>
      <a class="btn btn-ghost btn-lg" href="#models">Explore Models</a>
    </div>
  </div>
  <div class="hero-scroll">Scroll</div>
</section>

<div class="page-scope">
  <nav class="page-tabs" aria-label="Page sections">
    <div class="wrap">
      <a href="#models">Models</a>
      <a href="#promise">Warranty</a>
      <a href="#why">Why Chery</a>
    </div>
  </nav>

  <div id="models">
    <div class="wrap models-intro reveal">
      <div class="overline center">The range</div>
      <h2 class="section-title">The Tiggo family</h2>
      <p class="section-sub center">From the city-smart Tiggo 4 and its self-charging hybrid twin to the flagship Tiggo 9 — every Chery, backed by island-based service.</p>
    </div>
    {bands}
  </div>

  <section class="section showcase snap" id="inside">
    <div class="wrap">
      <div class="overline center reveal">Step inside</div>
      <h2 class="section-title center reveal">Cabins built for the climate</h2>
      <p class="section-sub center reveal" style="margin-inline:auto">Ventilated seats, panoramic light and quiet, screen-first cockpits — every Tiggo cabin is made for island driving.</p>
      <div class="showcase-grid">
        <figure class="sc-item reveal"><img src="{p}images/tiggo-9-int0.jpg" alt="Chery Tiggo 9 cabin" loading="lazy"></figure>
        <figure class="sc-item reveal"><img src="{p}images/tiggo-8-int4.jpg" alt="Chery Tiggo 8 first-class seating" loading="lazy"></figure>
        <figure class="sc-item reveal"><img src="{p}images/tiggo-7-int0.jpg" alt="Chery Tiggo 7 Pro interior" loading="lazy"></figure>
      </div>
    </div>
  </section>

  <section class="offer-strip offer-strip--photo fill snap" id="promise" style="--band-img:url('/images/band-warranty.jpg')">
    <div class="wrap">
      <div class="offer-head reveal">
        <div class="overline center light">The Chery promise</div>
        <h2 class="section-title">Own it with confidence</h2>
        <p class="section-sub center">Every new Chery comes with the strongest ownership package on the island.</p>
      </div>
      <div class="offer-row">{offer_items}</div>
      <div class="center reveal" style="margin-top:40px"><button class="btn btn-primary btn-lg" data-quote data-model="">Request a Quote</button></div>
    </div>
  </section>

  <section class="section why fill snap" id="why">
    <div class="row-bg"><img src="{p}images/tiggo-9-hero.jpg" alt="" aria-hidden="true" loading="lazy"></div>
    <div class="wrap">
      <div class="overline reveal">Peace of mind</div>
      <h2 class="section-title reveal">Why choose Chery</h2>
      <p class="section-sub reveal">Every Chery is backed by a team that's with you long after you drive off.</p>
      <div class="why-grid">{why_cards}</div>
    </div>
  </section>

  <section class="section fill snap">
    <div class="wrap">
      <div class="cta-band cta-band--photo reveal" style="--band-img:url('/images/band-cta.jpg')">
        <div class="txt">
          <h2>Start a wonderful life with Chery</h2>
          <p>Request a personalised quote or book a test drive at Chery Antigua — no obligation, about 30 seconds.</p>
        </div>
        <button class="btn btn-primary btn-lg" data-quote data-model="">Request a Quote</button>
      </div>
    </div>
  </section>
</div>

{footer(p)}
{floating()}
{modal()}
{scripts(p)}"""

    title = "Chery Antigua — Tiggo SUVs & Hybrids in St John's"
    desc = "Chery in Antigua & Barbuda — Tiggo 4, Tiggo 4 HEV, Tiggo 7 Pro, Tiggo 8 and the flagship Tiggo 9. 7-year warranty and local service in St John's."
    (ROOT / "index.html").write_text(head(title, desc, "", "index.html", jsonld=ld(home_ld()), preload=HERO_IMAGE) + body, encoding="utf-8")
    print("wrote index.html")

# ─────────────────────────────────────────────────────────── model pages
def build_model(m):
    p = "../"
    specs = "".join(
        f'<div class="spec"><div class="k">{E(k)}</div>'
        f'<div class="v">{E(v)}{(" <small>" + E(s) + "</small>") if s else ""}</div></div>'
        for k, v, s in m["specs"])
    features = "".join(
        f'<li>{IC_TICK}<span>{E(f)}</span></li>' for f in m["features"])

    offer_block = ""
    if m.get("feature_offer"):
        cells = "".join(
            f'<div class="offer-cell reveal"><div class="num">{E(o["big"])}</div>'
            f'<div class="lbl">{E(o["lbl"])}</div><div class="desc">{E(o["desc"])}</div></div>'
            for o in OFFER)
        offer_block = f"""
<section class="offer-strip">
  <div class="wrap">
    <div class="offer-head reveal">
      <div class="overline center">The Chery promise</div>
      <h2 class="section-title">Own it with confidence</h2>
      <p class="section-sub center">Every {E(m['name'])} comes with the strongest ownership package on the island.</p>
    </div>
    <div class="offer-row">{cells}</div>
  </div>
</section>"""

    # performance band — dark, big numbers (the cherysxm.com treatment)
    perf_cells = "".join(
        f'<div class="perf-cell reveal"><div class="pnum">{E(n)}<small>{E(u)}</small></div>'
        f'<div class="plbl">{E(l)}</div></div>'
        for n, u, l in m["perf"])

    gallery = "".join(
        f'<figure class="g-item reveal"><img src="{p}{g}" alt="Chery {E(m["name"])}" loading="lazy"></figure>'
        for g in m["gallery"])

    cockpit_tiles = "".join(
        f'<div class="ck-tile reveal"><div class="ck-v">{E(v)}</div><div class="ck-k">{E(k)}</div></div>'
        for v, k in m["cockpit"])
    int_imgs = "".join(
        f'<figure class="int-img reveal"><img src="{p}{im}" alt="Chery {E(m["name"])} interior" loading="lazy"></figure>'
        for im in m["interior"])

    # colour picker — swatch chips swap the stage. Colours with a 360 folder
    # (images/360/<slug>/<colour>/01..NN.jpg) get a drag-to-rotate spin viewer;
    # colours without one fall back to their static side view.
    colours = [(c + (None,))[:3] for c in (m.get("colours") or [])]
    colours_block = ""
    if colours:
        spin_frames = m.get("spin_frames", 0)
        spin_dir = m.get("spin_dir", m["slug"])   # HEV shares the Tiggo 4 sets
        first_name, first_img, first_spin = colours[0]
        chips = "".join(
            f'<button type="button" class="col-chip{" active" if i == 0 else ""}" data-colour="{p}{img}" '
            f'data-colour-name="{E(name)}"'
            + (f' data-spin-base="{p}images/360/{spin_dir}/{spin}"' if (spin and spin_frames) else "")
            + f'><img src="{p}{img}" alt="{E(m["name"])} in {E(name)}" loading="lazy">'
            f'<span>{E(name)}</span></button>'
            for i, (name, img, spin) in enumerate(colours))
        has_spin = spin_frames and any(s for _, _, s in colours)
        if has_spin and first_spin:
            first_stage_src = f"{p}images/360/{spin_dir}/{first_spin}/01.jpg"
        else:
            first_stage_src = f"{p}{first_img}"
        spin_attrs = f' data-frames="{spin_frames}"' if has_spin else ""
        spin_cls = " spin-stage" if has_spin else ""
        hint = '<div class="spin-hint"><svg viewBox="0 0 24 24" width="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v5h-5"/></svg> Drag to rotate</div>' if has_spin else ""
        colours_block = f"""
<section class="section colours-band" id="colours">
  <div class="wrap">
    <div class="overline reveal">Colours{' · 360°' if has_spin else ''}</div>
    <h2 class="section-title reveal">Make it yours</h2>
    <div class="colour-stage{spin_cls} reveal"{spin_attrs}>
      <img src="{first_stage_src}" alt="Chery {E(m['name'])} in {E(first_name)}" draggable="false">
      {hint}
    </div>
    <div class="colour-name">{E(first_name)}</div>
    <div class="col-chips reveal">{chips}</div>
  </div>
</section>"""

    # lux mosaic gallery (models without a 360 set — e.g. Tiggo 9)
    lux = m.get("lux_gallery") or []
    lux_block = ""
    if lux:
        cells = "".join(
            f'<figure class="lux-item {cls}"><img src="{p}{src}" alt="Chery {E(m["name"])} — {E(cap)}" loading="lazy">'
            f'<figcaption>{E(cap)}</figcaption></figure>'
            for src, cls, cap in lux)
        lux_block = f"""
<section class="section lux-band" id="gallery">
  <div class="wrap">
    <div class="overline reveal">Gallery</div>
    <h2 class="section-title reveal">The flagship, in detail</h2>
    <div class="lux-grid reveal">{cells}</div>
  </div>
</section>"""

    body = f"""
{header(p)}

<section class="mhero">
  <div class="mhero-bg"><img src="{p}{m['hero']}" alt="Chery {E(m['name'])}" fetchpriority="high" decoding="async"></div>
  <div class="back-link wrap"><a href="/models/">← All models</a></div>
  <div class="mhero-inner wrap">
    <h1 class="reveal in">Chery {E(m['name'])}</h1>
    <div class="mtag reveal in">{E(m['tagline'])}</div>
    <div class="mhero-cta reveal in">
      <button class="btn btn-primary btn-lg" data-quote data-model="{E(m['name'])}">Request a Quote</button>
      <a class="btn btn-ghost btn-lg" data-wa data-model="{E(m['name'])}" target="_blank" rel="noopener">WhatsApp us</a>
      <a class="btn btn-ghost btn-lg" href="/brochures/pdf/{m['slug']}.pdf" download target="_blank" rel="noopener">Download Brochure</a>
    </div>
  </div>
</section>

<section class="spec-band">
  <div class="wrap"><div class="spec-row">{specs}</div></div>
</section>

<section class="section intro-split">
  <div class="wrap feature-split">
    <div class="reveal">
      <div class="overline">{E(m['type'])}</div>
      <h2 class="section-title" style="font-size:clamp(28px,3.6vw,44px)">{E(m['tagline'])}</h2>
      <p class="section-sub" style="margin-top:14px">{E(m['lede'])}</p>
    </div>
    <div class="reveal">
      <ul class="feature-list">{features}</ul>
    </div>
  </div>
</section>

<section class="perf-band">
  <div class="wrap">
    <div class="overline light reveal">Performance</div>
    <h2 class="perf-title reveal">{E(m['perf_line'])}</h2>
    <div class="perf-row">{perf_cells}</div>
  </div>
</section>

<section class="gallery-strip">
  <div class="g-grid">{gallery}</div>
</section>

{colours_block}

{lux_block}

<section class="section cockpit">
  <div class="wrap">
    <div class="overline reveal">Interior</div>
    <h2 class="section-title reveal">Smart, spacious cockpit</h2>
    <div class="ck-row">{cockpit_tiles}</div>
    <div class="int-grid">{int_imgs}</div>
    <p class="disclaimer reveal">{E(DISCLAIMER)}</p>
  </div>
</section>

{offer_block}

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta-band cta-band--photo reveal" style="--band-img:url('/{m['hero']}')">
      <div class="txt">
        <h2>Ready to drive the {E(m['name'])}?</h2>
        <p>Request a personalised quote or book a test drive at Chery Antigua — no obligation, about 30 seconds.</p>
      </div>
      <button class="btn btn-primary btn-lg" data-quote data-model="{E(m['name'])}">Request a Quote</button>
    </div>
  </div>
</section>

{footer(p)}
{floating()}
{modal(selected=m['name'])}
{scripts(p)}"""

    title = f"{BRAND} {m['name']} — {m['seo_type']} | {SITE_NAME}"
    desc = m["seo_desc"]
    crumbs = breadcrumb_ld([("Home", BASE_URL + "/"),
                            ("Models", canonical("models/index.html")),
                            (f"{BRAND} {m['name']}", canonical(f"models/{m['slug']}.html"))])
    (ROOT / "models" / f"{m['slug']}.html").write_text(
        head(title, desc, p, f"models/{m['slug']}.html",
             jsonld=ld(vehicle_ld(m), crumbs),
             share_image=m.get("hero") or m.get("image"),
             preload=m.get("hero") or m.get("image")) + body, encoding="utf-8")
    print(f"wrote models/{m['slug']}.html")

# ───────────────────────────────────────────────────────── model brochures
CONTACT_PHONE = "+1 (268) 464-3345"   # WhatsApp / Tel

def brochure_head(title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{E(title)}</title>
  <meta name="robots" content="noindex, follow">
  <link rel="icon" type="image/png" href="../images/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/brochure.css">
</head>
<body class="brochure">"""

def build_brochure(m):
    p = "../"
    logo_white = f'<img src="{p}images/chery-logo-white.png" alt="Chery">'
    logo_dark = f'<img src="{p}images/chery-logo.png" alt="Chery">'
    specs = "".join(
        f'<div class="b-spec"><div class="k">{E(k)}</div>'
        f'<div class="v">{E(v)}{(" <small>"+E(s)+"</small>") if s else ""}</div></div>'
        for k, v, s in m["specs"])
    feats = "".join(f'<li>{IC_TICK}<span>{E(f)}</span></li>' for f in m["features"])
    offer = ""
    if m.get("feature_offer"):
        cells = "".join(
            f'<div class="ocell"><div class="num">{E(o["big"])}</div><div class="lbl">{E(o["lbl"])}</div></div>'
            for o in OFFER)
        offer = (f'<div class="b-offer"><div class="oh">The Chery promise</div>'
                 f'<div class="orow">{cells}</div></div>')

    tech_html = ""
    tech = TECH.get(m["slug"], [])
    if tech:
        # standard/boolean equipment shows a tick, not the word "Standard"
        tick = ('<svg class="tk" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
        def dv(v):
            return f'<span class="ok">{tick}</span>' if v == "Standard" else E(v)
        cats = "".join(
            f'<div class="tech-cat"><div class="tech-cat-h">{E(cat)}</div><dl class="tech-list">'
            + "".join(f'<div class="tr"><dt>{E(k)}</dt><dd>{dv(v)}</dd></div>' for k, v in rows)
            + "</dl></div>"
            for cat, rows in tech)
        tech_html = f'<div class="b-h3">Technical specifications</div>{cats}'

    body = f"""
<div class="sheet cover">
  <div class="cover-bg"><img src="{p}{m['hero']}" alt="Chery {E(m['name'])}"></div>
  <div class="cover-top">
    <div class="brand-lockup">{logo_white}</div>
    <div class="since">Antigua</div>
  </div>
  <div class="cover-foot">
    <div class="tag">{E(m['type'])}</div>
    <h1>{E(m['name'])}</h1>
    <div class="tl">{E(m['tagline'])}</div>
  </div>
</div>

<div class="sheet detail">
  <div class="d-head">
    <div class="d-brand">{logo_dark}</div>
    <div class="d-type">{E(m['type'])}</div>
  </div>
  <h2>{E(m['name'])}</h2>
  <p class="lead">{E(m['lede'])}</p>
  <div class="d-img"><img src="{p}{m['image']}" alt="Chery {E(m['name'])}"></div>

  <div class="b-h3">Key specifications</div>
  <div class="spec-grid">{specs}</div>

  <div class="b-h3">What you'll love</div>
  <ul class="feat-grid">{feats}</ul>

  {offer}

  {tech_html}

  <div class="b-contact">
    <div class="row">
      <div class="c-brand">{logo_dark}</div>
      <div class="c-info">
        <b>{E(SITE['showroom'][0])}</b><br>
        {'<br>'.join(E(l) for l in SITE['showroom'][1:])}<br>
        WhatsApp: {E(CONTACT_PHONE)}<br>
        <a href="mailto:{SITE['email']}">{E(SITE['email'])}</a> &nbsp;·&nbsp; {E(SITE['domain'])}
      </div>
    </div>
    <p class="b-disc">{E(DISCLAIMER)}</p>
  </div>
</div>

<div class="print-bar no-print">
  <button class="print-btn primary" onclick="window.print()">Save / Print as PDF</button>
</div>
</body>
</html>"""
    (ROOT / "brochures" / f"{m['slug']}.html").write_text(
        brochure_head(f"Chery {m['name']} — Brochure | Chery Antigua") + body, encoding="utf-8")
    print(f"wrote brochures/{m['slug']}.html")

# ─────────────────────────────────────────────────────── contact page
def build_contact():
    p = ""
    td_models = "".join(
        f'<label class="td-model"><input type="radio" name="model" value="{E(m["name"])}" required>'
        f'<span class="td-mcard"><span class="td-mthumb"><img src="{p}{m["image"]}" alt="Chery {E(m["name"])}" loading="lazy"></span>'
        f'<span class="td-minfo"><span class="nm">{E(m["name"])}</span><span class="ty">{E(m["type"])}</span></span>'
        f'<span class="td-check">{IC_TICK}</span></span></label>'
        for m in MODELS)
    msg_model_opts = "".join(f'<option value="{E(m["name"])}">{E(m["name"])}</option>' for m in MODELS)
    socials = (f'<a href="{SITE["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{IC_IG}</a>'
               f'<a href="{SITE["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook">{IC_FB}</a>')

    body = f"""
{header(p)}

<section class="contact-hero">
  <div class="wrap">
    <div class="overline reveal in">Chery · Antigua &amp; Barbuda</div>
    <h1 class="reveal in"><span class="sr-only">Contact Chery Antigua — </span>Get in touch</h1>
    <p class="c-lede reveal in">Book a test drive or send us a message — a member of our team will be in touch shortly.</p>
  </div>
</section>

<section class="section contact-main">
  <div class="wrap contact-grid">
    <aside class="contact-info reveal">
      <h2 class="sr-only">Visit Chery Antigua</h2>
      <div class="overline">Visit us</div>
      <p class="ci-line"><span class="ci-k">Address</span><span>{'<br>'.join(E(l) for l in SITE['showroom'])}</span></p>
      <p class="ci-line"><span class="ci-k">WhatsApp</span><a data-wa data-model="" target="_blank" rel="noopener">+1 (268) 464-3345</a></p>
      <p class="ci-line"><span class="ci-k">Email</span><a href="mailto:{SITE['email']}">{E(SITE['email'])}</a></p>
      <a class="btn btn-primary" data-wa data-model="" target="_blank" rel="noopener" style="margin-top:24px">{IC_WA_SM} Chat on WhatsApp</a>
      <div class="socials" style="margin-top:24px">{socials}</div>
    </aside>

    <div class="contact-card reveal">
      <div class="cc-tabs">
        <button type="button" class="cc-tab active" data-tab="testdrive">Book a Test Drive</button>
        <button type="button" class="cc-tab" data-tab="message">Send a Message</button>
      </div>

      <div class="cc-pane" data-pane="testdrive">
        <h2 class="sr-only">Book a test drive</h2>
        <div class="td-progress">
          <div class="td-bar"><span></span></div>
          <div class="td-steplabel">Step <b class="td-cur">1</b> of 3&nbsp;·&nbsp;<span class="td-title">Choose your model</span></div>
        </div>
        <form id="tdForm" novalidate>
          <input class="hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="td-panel" data-step="1">
            <div class="td-models">{td_models}</div>
          </div>
          <div class="td-panel" data-step="2" hidden>
            <div class="field"><label>Preferred date <span class="opt">(Mon–Fri)</span></label><input type="date" name="date" required></div>
            <div class="field"><label>Preferred time</label>
              <div class="td-chips">
                <label class="td-chip"><input type="radio" name="time" value="Morning (9am–12pm)" required><span>Morning</span></label>
                <label class="td-chip"><input type="radio" name="time" value="Afternoon (12–3pm)"><span>Afternoon</span></label>
                <label class="td-chip"><input type="radio" name="time" value="Late afternoon (3–5pm)"><span>Late afternoon</span></label>
              </div>
            </div>
            <div class="field"><label>Notes <span class="opt">(optional)</span></label><textarea name="notes" placeholder="Anything we should know?"></textarea></div>
          </div>
          <div class="td-panel" data-step="3" hidden>
            <div class="row-2">
              <div class="field"><label>First name</label><input name="firstName" required autocomplete="given-name" placeholder="Jane"></div>
              <div class="field"><label>Last name</label><input name="lastName" autocomplete="family-name" placeholder="Doe"></div>
            </div>
            <div class="field"><label>Phone / WhatsApp</label><input name="phone" type="tel" required autocomplete="tel" placeholder="+1 (268) 464-3345"></div>
            <div class="field"><label>Email</label><input name="email" type="email" required autocomplete="email" placeholder="you@email.com"></div>
          </div>
          <div class="td-nav">
            <button type="button" class="btn btn-outline td-back" hidden>← Back</button>
            <button type="button" class="btn btn-primary td-next">Next →</button>
            <button type="submit" class="btn btn-primary td-submit" hidden>Confirm booking →</button>
          </div>
          <p class="form-fine">By submitting you agree to be contacted by {E(SITE['dealer'])}.</p>
        </form>
        <div class="cc-done td-done" hidden>
          <div class="check">&#10003;</div>
          <h3>Test drive requested!</h3>
          <p>Thanks <span class="td-name">there</span> — we've received your request for the <b class="td-model-name">Chery</b>. Our team will confirm your slot shortly.</p>
          <a class="btn btn-outline" href="/">Back to home</a>
        </div>
      </div>

      <div class="cc-pane" data-pane="message" hidden>
        <h2 class="sr-only">Send us a message</h2>
        <form id="msgForm" novalidate>
          <input class="hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="row-2">
            <div class="field"><label>First name</label><input name="firstName" required autocomplete="given-name" placeholder="Jane"></div>
            <div class="field"><label>Last name</label><input name="lastName" autocomplete="family-name" placeholder="Doe"></div>
          </div>
          <div class="field"><label>Email</label><input name="email" type="email" required autocomplete="email" placeholder="you@email.com"></div>
          <div class="field"><label>Phone / WhatsApp <span class="opt">(optional)</span></label><input name="phone" type="tel" autocomplete="tel" placeholder="+1 (268) 464-3345"></div>
          <div class="field"><label>Model <span class="opt">(optional)</span></label><select name="model"><option value="">General enquiry</option>{msg_model_opts}</select></div>
          <div class="field"><label>Message</label><textarea name="message" required placeholder="How can we help?"></textarea></div>
          <button type="submit" class="btn btn-primary" style="width:100%">Send Message →</button>
          <p class="form-fine">By submitting you agree to be contacted by {E(SITE['dealer'])}.</p>
        </form>
        <div class="cc-done msg-done" hidden>
          <div class="check">&#10003;</div>
          <h3>Message sent!</h3>
          <p>Thanks <span class="msg-name">there</span> — we'll get back to you shortly.</p>
          <a class="btn btn-outline" href="/">Back to home</a>
        </div>
      </div>
    </div>
  </div>
</section>

{footer(p)}
{floating()}
{modal()}
{scripts(p, extra='<script src="assets/contact.js"></script>')}"""

    title = "Contact & Test Drive — Chery Antigua, St John's"
    desc = "Book a Chery test drive in St John's, Antigua — choose your Tiggo and a time, or message us. Showroom at the CMS Auto Complex, Scott's Hill Road."
    extra = '\n  <link rel="stylesheet" href="assets/contact.css">'
    (ROOT / "contact.html").write_text(
        head(title, desc, "", "contact.html", extra_head=extra,
             jsonld=ld(contact_ld())) + body, encoding="utf-8")
    print("wrote contact.html")

# ─────────────────────────────────────────────────────────────────── main
if __name__ == "__main__":
    (ROOT / "models").mkdir(exist_ok=True)
    (ROOT / "brochures").mkdir(exist_ok=True)
    build_home()
    build_models_index()
    build_404()
    build_seo_files()
    build_contact()
    for m in MODELS:
        build_model(m)
        build_brochure(m)
    add_image_dimensions()
    print("done —", len(MODELS), "models + brochures + contact")
