# Unified output schema for KURGIN Score Analyzer.
# Purpose: make one-stone screen, PDF, Excel and future platform card use the same semantic structure.

REPORT_SCHEMA_VERSION = "KURGIN Unified Report Schema v1.9.7"

IDENTIFICATION_COLUMNS = [
    "KURGIN Import ID",
    "Stone Title",
    "Identification Line",
    "Stock #",
    "Availability",
    "Report #",
    "Lab",
    "Shape",
]

CERTIFICATE_COLUMNS = [
    "Weight",
    "Color",
    "Clarity",
    "Cut",
    "Polish",
    "Symmetry",
    "Fluorescence",
    "Fluorescence Intensity",
    "Fluorescence Color",
    "Measurements",
    "Treatment",
    "Growth Method",
    "Diamond Type",
    "Inscription",
    "Cert comment",
    "CertFile",
    "Hearts & Arrows",
    "Report Issue Date",
    "Report Type",
    "Is Matched Pair Separable",
    "Origin Type",
    "Luster",
    "Category",
    "Country of Polishing",
    "Member Comment",
]

VISUAL_CERTIFICATE_COLUMNS = [
    "Shade",
    "Milky",
    "Eye Clean",
    "BGM",
    "KeyToSymbols",
    "White Inclusion",
    "Black Inclusion",
    "Open Inclusion",
]

GEOMETRY_COLUMNS = [
    "DepthPercent",
    "TablePercent",
    "CrownPercent",
    "CrownAngle",
    "PavilionPercent",
    "PavilionAngle",
    "GirdlePercent",
    "GirdleThin",
    "GirdleThick",
    "GirdleCondition",
    "CuletSize",
    "CuletCondition",
    "MinDiameter",
    "MaxDiameter",
    "AvgDiameter",
    "DepthMM",
    "DiameterDiff",
    "RoundnessDeviation",
    "Length",
    "Width",
    "Height",
    "Ratio",
]

SCORE_COLUMNS = [
    "Kurgin Score",
    "Verdict Local",
    "score_band_label_ru",
    "score_band",
    "Triple Score",
    "Structure Modifier",
    "Visual Check",
    "Critical Risk",
]

RISK_COLUMNS = [
    "Nailhead",
    "Fisheye",
    "Fire Loss",
    "Depth Dev",
    "Crown Dev",
    "Pavilion Dev",
    "Balance Err",
    "Girdle Penalty",
]

TAG_COLUMNS = [
    "tags_all",
    "tag1",
    "tag2",
    "tag3",
    "tag4",
    "tag5",
    "tag6",
    "tag_light",
    "tag_structure",
    "tag_spread",
    "tag_risk",
    "tag_certificate",
    "tag_commercial",
    "certificate_flags",
]

ANALYSIS_ELEMENT_COLUMNS = [
    "KURGIN Analysis Elements Version",
    "Fire Profile",
    "Fire Explanation RU",
    "Fire Explanation EN",
    "Brilliance Profile",
    "Brilliance Explanation RU",
    "Brilliance Explanation EN",
    "Contrast Profile",
    "Contrast Explanation RU",
    "Contrast Explanation EN",
    "Balance Profile",
    "Balance Explanation RU",
    "Balance Explanation EN",
    "Perfect Build Status",
    "Perfect Build Explanation RU",
    "Perfect Build Explanation EN",
    "Hidden Weight Status",
    "Hidden Weight Explanation RU",
    "Hidden Weight Explanation EN",
    "Nailhead Risk Status",
    "Nailhead Risk Explanation RU",
    "Nailhead Risk Explanation EN",
    "Fisheye Risk Status",
    "Fisheye Risk Explanation RU",
    "Fisheye Risk Explanation EN",
    "Low Fire Status",
    "Low Fire Explanation RU",
    "Low Fire Explanation EN",
    "Active KURGIN Tags",
    "Card Tags",
]


TEXT_COLUMNS = [
    "executive_summary_ru",
    "interpretation_short_ru",
    "interpretation_detail_ru",
    "recommendation_ru",
    "warning_ru",
    "disclaimer_ru",
]

REPORT_META_COLUMNS = [
    "price_usd",
    "price_per_carat_usd",
    "supplier",
    "Data Completeness %",
    "Report Quality Status",
    "KURGIN Report ID",
    "PDF Report Status",
    "PDF Report File",
    "PDF Report URL",
    "PDF Generation Mode",
    "Report Template Version",
    "Formula Output Version",
    "Engine Version",
    "Calculation Status",
    "Validation Errors",
]

FUTURE_MODULE_COLUMNS = [
    "spread_score",
    "spread_status",
    "diameter_symmetry_score",
    "diameter_symmetry_status",
    "roundness_status",
    "commercial_view",
    "value_score",
]

UNIFIED_REPORT_COLUMNS = (
    IDENTIFICATION_COLUMNS
    + CERTIFICATE_COLUMNS
    + VISUAL_CERTIFICATE_COLUMNS
    + GEOMETRY_COLUMNS
    + SCORE_COLUMNS
    + RISK_COLUMNS
    + TAG_COLUMNS
    + ANALYSIS_ELEMENT_COLUMNS
    + TEXT_COLUMNS
    + REPORT_META_COLUMNS
    + FUTURE_MODULE_COLUMNS
)

# Compact one-stone/card view.
KURGIN_CARD_COLUMNS = [
    "Stone Title",
    "Identification Line",
    "Kurgin Score",
    "Verdict Local",
    "score_band_label_ru",
    "Fire Profile",
    "Brilliance Profile",
    "Contrast Profile",
    "Balance Profile",
    "Card Tags",
    "Active KURGIN Tags",
    "tags_all",
    "interpretation_short_ru",
    "recommendation_ru",
    "Data Completeness %",
    "Report Quality Status",
    "PDF Report Status",
]

SECTION_ORDER = [
    ("Identification", IDENTIFICATION_COLUMNS),
    ("Certificate Data", CERTIFICATE_COLUMNS),
    ("Visual / Certificate Notes", VISUAL_CERTIFICATE_COLUMNS),
    ("Geometry", GEOMETRY_COLUMNS),
    ("KURGIN Score", SCORE_COLUMNS),
    ("Risks", RISK_COLUMNS),
    ("Tags", TAG_COLUMNS),
    ("KURGIN Analysis Elements", ANALYSIS_ELEMENT_COLUMNS),
    ("Interpretation", TEXT_COLUMNS),
    ("Report Metadata", REPORT_META_COLUMNS),
    ("Future Modules", FUTURE_MODULE_COLUMNS),
]

DATA_DICTIONARY_ROWS = [
    ("KURGIN Import ID", "Stable internal import identifier for KURGIN Platform", "No", "Yes", "Yes", "Connects Excel row, stone card, analysis and PDF"),
    ("Stone Title", "Human-readable stone title", "No", "Yes", "Yes", "Used in one-stone card and PDF title"),
    ("Identification Line", "Lab and report number line", "No", "Yes", "Yes", "Used in PDF and cards"),
    ("Stock #", "Supplier or inventory ID", "No", "Yes", "Yes", "Catalog identifier"),
    ("Report #", "Laboratory report number", "No", "Yes", "Yes", "Certificate reference"),
    ("Lab", "Laboratory name", "No", "Yes", "Yes", "IGI/GIA/other lab"),
    ("Shape", "Diamond shape", "Yes", "Yes", "Yes", "Current score supports ROUND"),
    ("Weight", "Carat weight", "No", "Yes", "Yes", "Shown separately, not part of core score"),
    ("Color", "Color grade", "No", "Yes", "Yes", "Shown separately, not part of core score"),
    ("Clarity", "Clarity grade", "No", "Yes", "Yes", "Shown separately, not part of core score"),
    ("Cut / Polish / Symmetry", "Certificate grades", "No", "Yes", "Yes", "Certificate characteristics"),
    ("Fluorescence", "Fluorescence data", "No", "Yes", "Yes", "Certificate/visual flag only"),
    ("Measurements", "Raw dimensions text", "Indirect", "Yes", "Yes", "Parsed into diameter/depth metrics"),
    ("DepthPercent / TablePercent", "Core proportions", "Yes", "Yes", "Yes", "Used in geometry/structure analysis"),
    ("CrownAngle / PavilionAngle", "Main optical angles", "Yes", "Yes", "Yes", "Used in KURGIN Score"),
    ("CrownPercent / PavilionPercent", "Height/depth proportions", "Yes", "Yes", "Yes", "Used in structure analysis"),
    ("GirdlePercent", "Girdle percentage", "Yes", "Yes", "Yes", "Used in structure/risk analysis"),
    ("MinDiameter / MaxDiameter / AvgDiameter", "Parsed round dimensions", "Planned", "Yes", "Yes", "Future spread/roundness modules"),
    ("RoundnessDeviation", "Diameter deviation percentage", "Planned", "Yes", "Yes", "Future diameter symmetry module"),
    ("Kurgin Score", "Main KURGIN optical/geometric score", "Output", "Yes", "Yes", "Core result"),
    ("Verdict Local", "Localized score verdict", "Output", "Yes", "Yes", "Human-readable result"),
    ("Score Band", "Score range label", "Output", "Yes", "Yes", "Used for stable interpretation tone"),
    ("tags_all / tag1-tag6", "Generated analysis tags", "Output", "Yes", "Yes", "Used for filtering and interpretations"),
    ("tag_light / tag_structure / tag_risk", "Categorized tags", "Output", "Yes", "Yes", "Used for platform filters"),
    ("interpretation_short_ru", "Short Russian interpretation", "Output", "Yes", "Yes", "Card/report text"),
    ("interpretation_detail_ru", "Detailed Russian interpretation", "Output", "Yes", "Yes", "Full report text"),
    ("recommendation_ru", "Recommendation text", "Output", "Yes", "Yes", "Selection guidance"),
    ("warning_ru", "Warning text", "Output", "Yes", "Yes", "Risk communication"),
    ("Data Completeness %", "Completeness of source data", "No", "Yes", "Yes", "Explains report quality"),
    ("Report Quality Status", "Complete / Partial / Geometry Only / etc.", "No", "Yes", "Yes", "Explains missing-data quality"),
    ("PDF Report Status", "PDF availability status", "No", "Yes", "Yes", "ready_to_generate / not_available"),
    ("PDF Report File", "Relative PDF path in package", "No", "Yes", "Yes", "reports/...pdf"),
    ("PDF Generation Mode", "How platform should generate PDF", "No", "Yes", "Yes", "on_demand recommended"),
    ("Engine Version", "Formula engine version", "Output", "Yes", "Yes", "Reproducibility"),
    ("Hearts & Arrows", "Hearts and Arrows supplier flag", "No", "Yes", "Yes", "Shown separately as visual/certificate characteristic"),
    ("Length / Width / Height", "Separate dimensions from supplier feed", "Indirect", "Yes", "Yes", "Used to derive diameter metrics when Measurements is missing"),
    ("price_per_carat_usd", "Supplier price per carat", "No", "No", "Yes", "Commercial field, not part of KURGIN Score"),
    ("price_usd", "Supplier total price", "No", "No", "Yes", "Commercial field, not part of KURGIN Score"),
    ("Report Issue Date / Report Type", "Certificate metadata", "No", "Yes", "Yes", "Useful for platform cards and data quality"),
    ("Origin Type / Growth Method", "Lab-grown/source information", "No", "Yes", "Yes", "Shown separately, not part of KURGIN Score"),
    ("Formula Output Version", "Excel/output schema version", "No", "Yes", "Yes", "Import compatibility"),
]


def select_existing(df, columns):
    return [col for col in columns if col in df.columns]
