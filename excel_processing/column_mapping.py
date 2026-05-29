import re
import pandas as pd

# Supplier upload recognition map.
# This file intentionally supports many supplier/lab aliases while preserving a stable internal schema.
CANONICAL_COLUMNS = {
    # Identification
    "Stock #": [
        "stock #", "stock#", "stock", "stock no", "stock number", "stock id",
        "lot", "lot #", "item", "item #", "sku"
    ],
    "Availability": ["availability", "status", "available", "наличие", "доступность"],
    "Location": ["location", "местоположение", "место"],
    "Country": ["country", "страна"],
    "State": ["state", "region", "область", "регион"],
    "City": ["city", "город"],
    "Country of Polishing": ["countryofpolishing", "country of polishing", "polishing country"],
    "Lab": ["lab", "laboratory", "cert lab", "certificate lab", "лаборатория"],
    "Report #": [
        "report #", "report", "report number", "certificate", "certificate number",
        "certificate #", "certificate#", "cert no", "cert number", "cert #",
        "igi report", "gia report", "номер сертификата", "сертификат"
    ],

    # Certificate / commercial fields
    "Shape": ["shape", "cut shape", "form", "форма", "огранка"],
    "Weight": ["weight", "carat", "carat weight", "ct", "вес", "карат"],
    "Color": ["color", "colour", "цвет"],
    "Clarity": ["clarity", "чистота"],
    "Cut": ["cut", "cut grade", "cutgrade", "качество огранки", "огранка класс"],
    "Polish": ["polish", "полировка"],
    "Symmetry": ["symmetry", "симметрия"],
    "Hearts & Arrows": ["h&a", "ha", "hearts & arrows", "hearts and arrows", "heart and arrow"],
    "Fluorescence": ["fluorescence", "fluor", "флуоресценция"],
    "Fluorescence Intensity": [
        "fluorescence intensity", "fluorescenceintensity", "fluor intensity",
        "fluorescence grade", "fluor grade", "floro", "flouro", "flo"
    ],
    "Fluorescence Color": ["fluorescence color", "fluor color", "fluorescence colour"],
    "Measurements": [
        "measurements", "measurement", "measurements mm", "size", "dimensions",
        "размеры", "измерения"
    ],
    "Length": ["length", "len"],
    "Width": ["width"],
    "Height": ["height", "depth mm raw", "measurement height"],
    "Ratio": ["ratio", "l/w", "l:w", "length width ratio"],
    "MinDiameter": ["min diameter", "mindiameter", "min dia", "mindia", "diameter min", "diameter_min", "d min", "minimum diameter"],
    "MaxDiameter": ["max diameter", "maxdiameter", "max dia", "maxdia", "diameter max", "diameter_max", "d max", "maximum diameter"],
    "AvgDiameter": ["avg diameter", "average diameter", "avgdiameter", "average dia", "avg dia", "diameter avg", "diameter average"],
    "DepthMM": ["depth mm", "depthmm", "height mm", "heightmm", "stone height", "measurement depth", "depth millimeter"],
    "DiameterDiff": ["diameter diff", "diameter difference", "diameterdiff", "roundness diff"],
    "RoundnessDeviation": ["roundness deviation", "roundnessdeviation", "roundness %", "diameter deviation", "diameter deviation %"],
    "Treatment": ["treatment", "treated", "облагораживание", "обработка"],
    "Growth Method": [
        "growth method", "growth", "growthtype", "growth type", "method",
        "cvd/hpht", "process"
    ],
    "Origin Type": ["type", "origin type", "stone type", "diamond origin"],
    "Diamond Type": ["diamond type", "тип алмаза"],
    "Luster": ["luster", "lustre"],
    "Category": ["category", "категория"],
    "Inscription": ["inscription", "laser inscription", "laserinscription", "laser", "надпись"],
    "Cert comment": [
        "cert comment", "certcomment", "certificate comment", "comments", "comment",
        "remarks", "note", "notes"
    ],
    "Member Comment": ["member comment", "membercomment", "supplier comment", "vendor comment"],
    "CertFile": [
        "certfile", "cert file", "certificate file", "certificatefilename",
        "certificate filename", "pdf", "certificate pdf", "cert link"
    ],
    "Report Issue Date": ["reportissuedate", "report issue date", "issue date", "certificate date"],
    "Report Type": ["reporttype", "report type", "certificate type"],
    "Is Matched Pair Separable": ["ismatchedpairseparable", "is matched pair separable", "matched pair separable"],

    # Visual flags / inclusions
    "Shade": ["shade", "оттенок"],
    "Milky": ["milky", "milkiness", "молочность"],
    "Eye Clean": ["eye clean", "eyeclean", "eye-clean", "визуально чистый"],
    "BGM": ["bgm", "brown green milky", "membercomment"],
    "KeyToSymbols": ["keytosymbols", "key to symbols", "key symbols", "symbols", "inclusion symbols"],
    "White Inclusion": ["white inclusion", "white inclusions", "white inc"],
    "Black Inclusion": ["black inclusion", "black inclusions", "black inc"],
    "Open Inclusion": ["open inclusion", "openinclusion", "open inclusions", "open inc"],
    "Fancy Color": ["fancy color", "fancycolor"],
    "Fancy Color Intensity": ["fancy color intensity", "fancycolorintensity"],
    "Fancy Color Overtone": ["fancy color overtone", "fancycolorovertone"],

    # Geometry / proportions
    "CrownAngle": ["crownangle", "crown angle", "crown ang", "crown_angle", "угол короны"],
    "PavilionAngle": ["pavilionangle", "pavilion angle", "pavilion ang", "pavilion_angle", "угол павильона"],
    "TablePercent": ["tablepercent", "table %", "table%", "table", "table percent", "table_pct", "площадка"],
    "DepthPercent": ["depthpercent", "depth %", "depth%", "depth", "depth percent", "depth_pct", "глубина"],
    "CrownPercent": [
        "crownpercent", "crown %", "crown height %", "crown height",
        "crownheight", "crown height percent", "crown_pct", "высота короны"
    ],
    "PavilionPercent": [
        "pavilionpercent", "pavilion %", "pavilion depth %", "pavilion depth",
        "paviliondepth", "pavilion depth percent", "pavilion_pct", "глубина павильона"
    ],
    "GirdlePercent": [
        "girdlepercent", "girdle %", "girdle%", "girdle", "girdle pct",
        "girdle percent", "рундист"
    ],
    "GirdleThin": ["girdlethin", "girdle thin", "thin girdle", "girdle min", "min girdle"],
    "GirdleThick": ["girdlethick", "girdle thick", "thick girdle", "girdle max", "max girdle"],
    "GirdleCondition": ["girdle condition", "girdlecondition", "girdle description", "girdle type"],
    "CuletSize": ["culet size", "culetsize", "culet", "калетта", "кулет"],
    "CuletCondition": ["culet condition", "culetcondition", "culet description"],

    # Media / commercial
    "Diamond Video": ["diamond video", "video", "video link"],
    "Diamond Image": ["diamond image", "image", "photo", "фото"],
    "price_rub": ["price_rub", "price rub", "price ₽", "rub", "цена руб", "цена"],
    "price_usd": ["price_usd", "price usd", "usd", "price $", "total", "total price"],
    "price_per_carat_usd": ["$/ct", "price per ct", "price/ct", "price per carat", "ppc", "rate"],
    "supplier": ["supplier", "vendor", "поставщик"],
}


def normalize_name(name):
    name = str(name).strip().lower()
    name = name.replace("\n", " ")
    name = re.sub(r"[_\-]+", " ", name)
    name = re.sub(r"\s+", " ", name)
    return name


def normalize_compact(name):
    return re.sub(r"[^a-z0-9а-я]+", "", normalize_name(name))


def build_alias_map():
    alias_map = {}
    for canonical, aliases in CANONICAL_COLUMNS.items():
        alias_map[normalize_name(canonical)] = canonical
        alias_map[normalize_compact(canonical)] = canonical
        for alias in aliases:
            alias_map[normalize_name(alias)] = canonical
            alias_map[normalize_compact(alias)] = canonical
    return alias_map


def apply_column_mapping(df):
    alias_map = build_alias_map()
    rename_map = {}
    mapped_targets = set(df.columns)
    mapping_rows = []

    for col in df.columns:
        normalized = normalize_name(col)
        compact = normalize_compact(col)
        canonical = alias_map.get(normalized) or alias_map.get(compact)

        if canonical and canonical not in mapped_targets:
            rename_map[col] = canonical
            mapped_targets.add(canonical)
            mapping_rows.append({
                "Original Column": col,
                "Mapped To": canonical,
                "Status": "mapped",
                "Confidence": 1.00,
                "Note": "recognized alias"
            })
        elif canonical and canonical == col:
            mapping_rows.append({
                "Original Column": col,
                "Mapped To": canonical,
                "Status": "already canonical",
                "Confidence": 1.00,
                "Note": "already in KURGIN schema"
            })
        elif canonical and canonical in mapped_targets:
            mapping_rows.append({
                "Original Column": col,
                "Mapped To": canonical,
                "Status": "duplicate target kept original",
                "Confidence": 0.85,
                "Note": "another column already mapped to this target"
            })
        else:
            mapping_rows.append({
                "Original Column": col,
                "Mapped To": "",
                "Status": "not mapped",
                "Confidence": 0.00,
                "Note": "not used by current analyzer"
            })

    mapped_df = df.rename(columns=rename_map)
    mapping_df = pd.DataFrame(mapping_rows)
    return mapped_df, mapping_df
