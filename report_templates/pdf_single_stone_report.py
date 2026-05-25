from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _register_font():
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                pdfmetrics.registerFont(TTFont("KurginSans", str(path)))
                return "KurginSans"
            except Exception:
                continue

    return "Helvetica"


FONT_NAME = _register_font()


def _safe(value, default="—"):
    if value is None:
        return default
    text = str(value)
    if text.lower() in ["nan", "none", ""]:
        return default
    return text


def _score(value):
    try:
        return f"{float(value):.2f}"
    except Exception:
        return "—"


def _row_value(row, *names, default="—"):
    for name in names:
        try:
            value = row.get(name, None)
        except Exception:
            value = None
        if value is not None and str(value).lower() not in ["nan", "none", ""]:
            return value
    return default


def _make_styles():
    styles = getSampleStyleSheet()

    return {
        "brand": ParagraphStyle(
            "brand",
            parent=styles["Title"],
            fontName=FONT_NAME,
            fontSize=28,
            leading=32,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0B1220"),
            spaceAfter=4,
        ),
        "title": ParagraphStyle(
            "title",
            parent=styles["Heading1"],
            fontName=FONT_NAME,
            fontSize=16,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=styles["BodyText"],
            fontName=FONT_NAME,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=18,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=styles["Heading2"],
            fontName=FONT_NAME,
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#0B1220"),
            spaceBefore=12,
            spaceAfter=7,
        ),
        "body": ParagraphStyle(
            "body",
            parent=styles["BodyText"],
            fontName=FONT_NAME,
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#111827"),
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "small": ParagraphStyle(
            "small",
            parent=styles["BodyText"],
            fontName=FONT_NAME,
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=6,
        ),
        "score": ParagraphStyle(
            "score",
            parent=styles["Title"],
            fontName=FONT_NAME,
            fontSize=40,
            leading=44,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#B8892E"),
            spaceAfter=4,
        ),
        "center": ParagraphStyle(
            "center",
            parent=styles["BodyText"],
            fontName=FONT_NAME,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=8,
        ),
    }


def _kv_table(rows, col_widths=None):
    data = [[Paragraph(str(k), _TABLE_KEY_STYLE), Paragraph(_safe(v), _TABLE_VALUE_STYLE)] for k, v in rows]
    table = Table(data, colWidths=col_widths or [55 * mm, 110 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F8FAFC")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111827")),
        ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#E5E7EB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 7.5)
    canvas.setFillColor(colors.HexColor("#94A3B8"))
    canvas.drawString(18 * mm, 12 * mm, "KURGIN Diamond Analysis Report")
    canvas.drawRightString(192 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


def _risk_label(value):
    if value in [True, "True", "YES", "Yes", "yes", 1]:
        return "Yes"
    if value in [False, "False", "NO", "No", "no", 0]:
        return "No"
    return _safe(value)


def create_single_stone_pdf(row, language="RU"):
    """
    Build branded PDF bytes for one diamond.
    The PDF does not expose internal coefficients or commercial formula rules.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="KURGIN Diamond Analysis Report",
    )

    styles = _make_styles()
    global _TABLE_KEY_STYLE, _TABLE_VALUE_STYLE
    _TABLE_KEY_STYLE = ParagraphStyle("table_key", fontName=FONT_NAME, fontSize=8.5, leading=11, textColor=colors.HexColor("#334155"))
    _TABLE_VALUE_STYLE = ParagraphStyle("table_value", fontName=FONT_NAME, fontSize=8.5, leading=11, textColor=colors.HexColor("#111827"))

    stone_title = _safe(_row_value(row, "Stone Title"), "Diamond Analysis")
    identification = _safe(_row_value(row, "Identification Line"), "")
    report_number = _safe(_row_value(row, "Report #"), "")
    lab = _safe(_row_value(row, "Lab"), "")
    score = _score(_row_value(row, "Kurgin Score"))
    verdict = _safe(_row_value(row, "Verdict Local", "Verdict"))
    tags = _safe(_row_value(row, "tags_all", "Tags Local", "Tags"), "")

    short_text = _safe(_row_value(row, "interpretation_short_ru", "interpretation_short_en"), "")
    detail_text = _safe(_row_value(row, "interpretation_detail_ru", "interpretation_detail_en"), "")
    recommendation = _safe(_row_value(row, "recommendation_ru", "recommendation_en"), "")
    warning = _safe(_row_value(row, "warning_ru", "warning_en"), "")
    disclaimer = _safe(_row_value(row, "disclaimer_ru", "disclaimer_en"), "")

    story = []

    # Page 1: Summary
    story.append(Paragraph("KURGIN", styles["brand"]))
    story.append(Paragraph("Diamond Analysis Report", styles["title"]))
    story.append(Paragraph("Аналитический отчёт по бриллианту", styles["subtitle"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(stone_title, styles["center"]))
    if identification:
        story.append(Paragraph(identification, styles["subtitle"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph(score, styles["score"]))
    story.append(Paragraph("KURGIN Score / 100", styles["center"]))
    story.append(Paragraph(f"<b>{verdict}</b>", styles["center"]))

    if tags:
        story.append(Spacer(1, 8))
        story.append(Paragraph(f"<b>Tags:</b> {tags}", styles["center"]))

    story.append(Spacer(1, 14))
    story.append(Paragraph("Краткий вывод", styles["h2"]))
    story.append(Paragraph(short_text, styles["body"]))

    if recommendation:
        story.append(Paragraph("Рекомендация", styles["h2"]))
        story.append(Paragraph(recommendation, styles["body"]))

    story.append(PageBreak())

    # Page 2: Certificate and geometry
    story.append(Paragraph("Данные камня", styles["h2"]))
    certificate_rows = [
        ("Stone Title", stone_title),
        ("Report #", report_number),
        ("Lab", lab),
        ("Shape", _row_value(row, "Shape")),
        ("Weight", _row_value(row, "Weight")),
        ("Color", _row_value(row, "Color")),
        ("Clarity", _row_value(row, "Clarity")),
        ("Cut", _row_value(row, "Cut")),
        ("Polish", _row_value(row, "Polish")),
        ("Symmetry", _row_value(row, "Symmetry")),
        ("Fluorescence", _row_value(row, "Fluorescence")),
        ("Measurements", _row_value(row, "Measurements")),
        ("Treatment", _row_value(row, "Treatment")),
        ("Growth Method", _row_value(row, "Growth Method")),
    ]
    story.append(_kv_table(certificate_rows))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Геометрия и пропорции", styles["h2"]))
    geometry_rows = [
        ("Table %", _row_value(row, "TablePercent", "Table %")),
        ("Depth %", _row_value(row, "DepthPercent", "Depth %")),
        ("Crown Angle", _row_value(row, "CrownAngle", "Crown Angle")),
        ("Pavilion Angle", _row_value(row, "PavilionAngle", "Pavilion Angle")),
        ("Crown %", _row_value(row, "CrownPercent", "Crown %")),
        ("Pavilion %", _row_value(row, "PavilionPercent", "Pavilion %")),
        ("Girdle %", _row_value(row, "GirdlePercent", "Girdle %")),
        ("Girdle Condition", _row_value(row, "GirdleCondition")),
        ("Culet Size", _row_value(row, "CuletSize")),
        ("Culet Condition", _row_value(row, "CuletCondition")),
    ]
    story.append(_kv_table(geometry_rows))

    story.append(PageBreak())

    # Page 3: KURGIN analysis and risks
    story.append(Paragraph("KURGIN Score Analysis", styles["h2"]))
    analysis_rows = [
        ("KURGIN Score", score),
        ("Verdict", verdict),
        ("Triple Score", _row_value(row, "Triple Score")),
        ("Structure Modifier", _row_value(row, "Structure Modifier")),
        ("Visual Check", _risk_label(_row_value(row, "Visual Check"))),
        ("Critical Risk", _risk_label(_row_value(row, "Critical Risk"))),
        ("Score Band", _row_value(row, "score_band_label_ru", "score_band_label_en")),
        ("Calculation Status", _row_value(row, "Calculation Status")),
        ("Engine Version", _row_value(row, "Engine Version")),
    ]
    story.append(_kv_table(analysis_rows))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Риски и предупреждения", styles["h2"]))
    risk_rows = [
        ("Nailhead Risk", _row_value(row, "Nailhead")),
        ("Fisheye Risk", _row_value(row, "Fisheye")),
        ("Fire Loss", _row_value(row, "Fire Loss")),
        ("Depth Deviation", _row_value(row, "Depth Dev")),
        ("Crown Deviation", _row_value(row, "Crown Dev")),
        ("Pavilion Deviation", _row_value(row, "Pavilion Dev")),
        ("Balance Error", _row_value(row, "Balance Err")),
        ("Girdle Penalty", _row_value(row, "Girdle Penalty")),
    ]
    story.append(_kv_table(risk_rows))

    if warning:
        story.append(Spacer(1, 8))
        story.append(Paragraph("Предупреждение", styles["h2"]))
        story.append(Paragraph(warning, styles["body"]))

    story.append(PageBreak())

    # Page 4: Interpretation and disclaimer
    story.append(Paragraph("Подробная интерпретация", styles["h2"]))
    for part in str(detail_text).split("\n"):
        if part.strip():
            story.append(Paragraph(part.strip(), styles["body"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Рекомендация KURGIN", styles["h2"]))
    story.append(Paragraph(recommendation, styles["body"]))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Ограничение анализа", styles["h2"]))
    story.append(Paragraph(disclaimer, styles["small"]))

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()