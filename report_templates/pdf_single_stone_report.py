
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


def _register_ttf(name, candidates):
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                pdfmetrics.registerFont(TTFont(name, str(path)))
                return name
            except Exception:
                continue
    return None


LATIN_FONT = _register_ttf('KurginLatin', [
    '/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    'C:/Windows/Fonts/arial.ttf',
]) or 'Helvetica'

ARMENIAN_FONT = _register_ttf('KurginArmenian', [
    '/usr/share/fonts/truetype/noto/NotoSansArmenian-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]) or LATIN_FONT

try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    CJK_FONT = 'STSong-Light'
except Exception:
    CJK_FONT = LATIN_FONT


ML = {
    'title': {
        'ru': 'Аналитический отчёт KURGIN',
        'en': 'KURGIN Diamond Analysis Report',
        'zh': 'KURGIN 钻石分析报告',
        'hy': 'KURGIN ադամանդի վերլուծական հաշվետվություն',
    },
    'stone_title': {'ru': 'Название камня', 'en': 'Stone title', 'zh': '钻石名称', 'hy': 'Քարի անվանում'},
    'report_number': {'ru': 'Номер сертификата', 'en': 'Report number', 'zh': '证书编号', 'hy': 'Սերտիֆիկատի համար'},
    'laboratory': {'ru': 'Лаборатория', 'en': 'Laboratory', 'zh': '实验室', 'hy': 'Լաբորատորիա'},
    'stock': {'ru': 'Stock #', 'en': 'Stock #', 'zh': '库存编号', 'hy': 'Պահեստային համար'},
    'short': {'ru': 'Краткий вывод', 'en': 'Short conclusion', 'zh': '简短结论', 'hy': 'Կարճ եզրակացություն'},
    'recommendation': {'ru': 'Рекомендация', 'en': 'Recommendation', 'zh': '建议', 'hy': 'Խորհուրդ'},
    'certificate_geometry': {'ru': 'Данные сертификата и геометрия', 'en': 'Certificate data and geometry', 'zh': '证书数据和几何参数', 'hy': 'Սերտիֆիկատի տվյալներ և երկրաչափություն'},
    'analysis_risks': {'ru': 'KURGIN-анализ и риски', 'en': 'KURGIN analysis and risks', 'zh': 'KURGIN 分析与风险', 'hy': 'KURGIN վերլուծություն և ռիսկեր'},
    'interpretation': {'ru': 'Интерпретация', 'en': 'Interpretation', 'zh': '解读', 'hy': 'Մեկնաբանություն'},
    'disclaimer': {'ru': 'Ограничение анализа', 'en': 'Disclaimer', 'zh': '分析限制', 'hy': 'Վերլուծության սահմանափակում'},
}

BAND_TEXTS = {
    'elite': {
        'zh': '该钻石在当前 KURGIN Score 模型下达到精英级结构水平。',
        'hy': 'Այս ադամանդը KURGIN Score-ի ընթացիկ մոդելով ցույց է տալիս էլիտար կառուցվածքի մակարդակ։',
    },
    'premium': {
        'zh': '该钻石显示出高端珠宝级的结构水平，可作为强候选。',
        'hy': 'Այս ադամանդը ցույց է տալիս պրեմիում զարդային մակարդակ և կարող է դիտարկվել որպես ուժեղ թեկնածու։',
    },
    'high': {
        'zh': '该钻石具有较高的结构质量，但仍建议与相近替代品比较。',
        'hy': 'Այս ադամանդը ունի բարձր կառուցվածքային որակ, սակայն ցանկալի է համեմատել մոտ այլընտրանքների հետ։',
    },
    'standard': {
        'zh': '该钻石属于标准商业范围，应结合价格、视觉效果和替代品比较。',
        'hy': 'Այս ադամանդը գտնվում է ստանդարտ առևտրային միջակայքում․ պետք է հաշվի առնել գինը, տեսողական ընկալումը և այլընտրանքները։',
    },
    'fair': {
        'zh': '该钻石为中等结果，选择时需要谨慎并与替代品比较。',
        'hy': 'Այս ադամանդը միջին արդյունք ունի․ ընտրության ժամանակ անհրաժեշտ է զգուշություն և համեմատություն այլընտրանքների հետ։',
    },
    'poor': {
        'zh': '该钻石在当前模型下显示出较低的结构质量，建议考虑更稳定的替代品。',
        'hy': 'Այս ադամանդը ընթացիկ մոդելով ցույց է տալիս ցածր կառուցվածքային որակ․ ցանկալի է դիտարկել ավելի կայուն այլընտրանքներ։',
    },
    'rejected': {
        'zh': '该钻石不建议用于珠宝级选择，除非有额外专业依据。',
        'hy': 'Այս ադամանդը խորհուրդ չի տրվում զարդային ընտրության համար՝ առանց լրացուցիչ մասնագիտական հիմնավորման։',
    },
    'not_calculated': {
        'zh': 'KURGIN Score 未计算。',
        'hy': 'KURGIN Score-ը չի հաշվարկվել։',
    },
}

RECOMMENDATION_TEXT = {
    'zh': '建议核验证书编号，并确认实物、照片或视频未显示不良视觉效果。',
    'hy': 'Խորհուրդ է տրվում ստուգել սերտիֆիկատի համարը և համոզվել, որ տեսողական զննումը, լուսանկարները կամ տեսանյութը չեն ցույց տալիս անցանկալի ազդեցություններ։',
}

DISCLAIMER_TEXT = {
    'ru': 'KURGIN Score не является лабораторным сертификатом и не заменяет заключение IGI, GIA или другой геммологической лаборатории. Анализ основан на параметрах, предоставленных пользователем, импортированных из таблицы или извлечённых из документа.',
    'en': 'KURGIN Score is not a laboratory certificate and does not replace an IGI, GIA or other gemological laboratory report. The analysis is based on parameters provided by the user, imported from a table or extracted from a document.',
    'zh': 'KURGIN Score 不是实验室证书，也不能替代 IGI、GIA 或其他宝石实验室报告。本分析基于用户提供、表格导入或文件提取的参数。',
    'hy': 'KURGIN Score-ը լաբորատոր սերտիֆիկատ չէ և չի փոխարինում IGI, GIA կամ այլ գեմոլոգիական լաբորատորիայի եզրակացությանը։ Վերլուծությունը հիմնված է օգտագործողի տրամադրած, աղյուսակից ներմուծված կամ փաստաթղթից ստացված տվյալների վրա։',
}


def _get_logo_path():
    current = Path(__file__).resolve()
    for candidate in [
        current.parents[1] / 'assets' / 'kurgin_logo.jpg',
        current.parents[1] / 'assets' / 'kurgin_logo.png',
    ]:
        if candidate.exists():
            return str(candidate)
    return None


def _safe(value, default='—'):
    if value is None:
        return default
    text = str(value).strip()
    if text.lower() in ['nan', 'none', '', '—', '-']:
        return default
    return text


def _score(value):
    try:
        return f'{float(value):.2f}'
    except Exception:
        return '—'


def _row_value(row, *names, default='—'):
    for name in names:
        try:
            value = row.get(name, None)
        except Exception:
            value = None
        if value is not None and str(value).strip().lower() not in ['nan', 'none', '', '—', '-']:
            return value
    return default


def _styles():
    return {
        'brand': ParagraphStyle('brand', fontName=LATIN_FONT, fontSize=23, leading=26, alignment=TA_CENTER, textColor=colors.HexColor('#0B1220'), spaceAfter=2),
        'title_ru': ParagraphStyle('title_ru', fontName=LATIN_FONT, fontSize=13, leading=15, alignment=TA_CENTER, textColor=colors.HexColor('#0B1220'), spaceAfter=1),
        'title_en': ParagraphStyle('title_en', fontName=LATIN_FONT, fontSize=9.5, leading=11, alignment=TA_CENTER, textColor=colors.HexColor('#334155'), spaceAfter=1),
        'title_zh': ParagraphStyle('title_zh', fontName=CJK_FONT, fontSize=9.3, leading=11, alignment=TA_CENTER, textColor=colors.HexColor('#334155'), spaceAfter=1),
        'title_hy': ParagraphStyle('title_hy', fontName=ARMENIAN_FONT, fontSize=8.7, leading=10.5, alignment=TA_CENTER, textColor=colors.HexColor('#334155'), spaceAfter=4),
        'h2_ru': ParagraphStyle('h2_ru', fontName=LATIN_FONT, fontSize=10.8, leading=12.5, textColor=colors.HexColor('#0B1220'), spaceBefore=5, spaceAfter=2),
        'h2_en': ParagraphStyle('h2_en', fontName=LATIN_FONT, fontSize=7.6, leading=9, textColor=colors.HexColor('#64748B'), spaceAfter=1),
        'h2_zh': ParagraphStyle('h2_zh', fontName=CJK_FONT, fontSize=7.4, leading=9, textColor=colors.HexColor('#64748B'), spaceAfter=1),
        'h2_hy': ParagraphStyle('h2_hy', fontName=ARMENIAN_FONT, fontSize=7.2, leading=8.8, textColor=colors.HexColor('#64748B'), spaceAfter=2),
        'body_ru': ParagraphStyle('body_ru', fontName=LATIN_FONT, fontSize=7.9, leading=10.2, textColor=colors.HexColor('#111827'), spaceAfter=2),
        'body_en': ParagraphStyle('body_en', fontName=LATIN_FONT, fontSize=7.4, leading=9.5, textColor=colors.HexColor('#334155'), spaceAfter=2),
        'body_zh': ParagraphStyle('body_zh', fontName=CJK_FONT, fontSize=7.1, leading=9.2, textColor=colors.HexColor('#334155'), spaceAfter=2),
        'body_hy': ParagraphStyle('body_hy', fontName=ARMENIAN_FONT, fontSize=7.1, leading=9.2, textColor=colors.HexColor('#334155'), spaceAfter=2),
        'small_ru': ParagraphStyle('small_ru', fontName=LATIN_FONT, fontSize=6.7, leading=8.4, textColor=colors.HexColor('#64748B'), spaceAfter=1),
        'small_en': ParagraphStyle('small_en', fontName=LATIN_FONT, fontSize=6.5, leading=8.2, textColor=colors.HexColor('#64748B'), spaceAfter=1),
        'small_zh': ParagraphStyle('small_zh', fontName=CJK_FONT, fontSize=6.4, leading=8.1, textColor=colors.HexColor('#64748B'), spaceAfter=1),
        'small_hy': ParagraphStyle('small_hy', fontName=ARMENIAN_FONT, fontSize=6.4, leading=8.1, textColor=colors.HexColor('#64748B'), spaceAfter=1),
        'score': ParagraphStyle('score', fontName=LATIN_FONT, fontSize=30, leading=33, alignment=TA_CENTER, textColor=colors.HexColor('#B8892E'), spaceAfter=0),
        'center': ParagraphStyle('center', fontName=LATIN_FONT, fontSize=8.0, leading=9.5, alignment=TA_CENTER, textColor=colors.HexColor('#111827'), spaceAfter=2),
        'muted_center': ParagraphStyle('muted_center', fontName=LATIN_FONT, fontSize=6.9, leading=8.5, alignment=TA_CENTER, textColor=colors.HexColor('#64748B'), spaceAfter=1),
        'tbl_key': ParagraphStyle('tbl_key', fontName=LATIN_FONT, fontSize=6.4, leading=8.0, textColor=colors.HexColor('#334155')),
        'tbl_val': ParagraphStyle('tbl_val', fontName=LATIN_FONT, fontSize=6.7, leading=8.4, textColor=colors.HexColor('#111827')),
        'tbl_key_zh': ParagraphStyle('tbl_key_zh', fontName=CJK_FONT, fontSize=5.8, leading=7.0, textColor=colors.HexColor('#64748B')),
        'tbl_key_hy': ParagraphStyle('tbl_key_hy', fontName=ARMENIAN_FONT, fontSize=5.8, leading=7.0, textColor=colors.HexColor('#64748B')),
    }


def _ml_heading(story, key, st):
    item = ML[key]
    story.append(Paragraph(item['ru'], st['h2_ru']))
    story.append(Paragraph(item['en'], st['h2_en']))
    story.append(Paragraph(item['zh'], st['h2_zh']))
    story.append(Paragraph(item['hy'], st['h2_hy']))


def _ml_label_cell(ru, en, zh, hy, st):
    return [
        Paragraph(f'<b>{ru}</b>', st['tbl_key']),
        Paragraph(en, st['tbl_key']),
        Paragraph(zh, st['tbl_key_zh']),
        Paragraph(hy, st['tbl_key_hy']),
    ]


def _kv_table(rows, key_w=44*mm, val_w=45*mm):
    st = _styles()
    data = [[_ml_label_cell(*labels, st), Paragraph(_safe(value), st['tbl_val'])] for labels, value in rows]
    table = Table(data, colWidths=[key_w, val_w], hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E5E7EB')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    return table


def _two_col(left_rows, right_rows):
    left = _kv_table(left_rows, key_w=37*mm, val_w=47*mm)
    right = _kv_table(right_rows, key_w=42*mm, val_w=45*mm)
    outer = Table([[left, right]], colWidths=[87*mm, 90*mm])
    outer.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    return outer


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(LATIN_FONT, 6.5)
    canvas.setFillColor(colors.HexColor('#94A3B8'))
    canvas.drawString(15*mm, 9*mm, 'KURGIN Analytical Report')
    canvas.drawRightString(195*mm, 9*mm, f'Page {doc.page}')
    canvas.restoreState()


def _band_key(row):
    key = _safe(_row_value(row, 'score_band'), '').lower().strip()
    if key:
        return key
    score = None
    try:
        score = float(_row_value(row, 'Kurgin Score'))
    except Exception:
        return 'not_calculated'
    if score >= 98.5: return 'elite'
    if score >= 95: return 'premium'
    if score >= 90: return 'high'
    if score >= 80: return 'standard'
    if score >= 70: return 'fair'
    if score >= 50: return 'poor'
    return 'rejected'


def _zh_summary(row):
    return BAND_TEXTS.get(_band_key(row), BAND_TEXTS['not_calculated'])['zh']


def _hy_summary(row):
    return BAND_TEXTS.get(_band_key(row), BAND_TEXTS['not_calculated'])['hy']


def _identity_card(row, st):
    rows = [
        ((ML['stone_title']['ru'], ML['stone_title']['en'], ML['stone_title']['zh'], ML['stone_title']['hy']), _row_value(row, 'Stone Title')),
        ((ML['report_number']['ru'], ML['report_number']['en'], ML['report_number']['zh'], ML['report_number']['hy']), _row_value(row, 'Report #')),
        ((ML['laboratory']['ru'], ML['laboratory']['en'], ML['laboratory']['zh'], ML['laboratory']['hy']), _row_value(row, 'Lab')),
        ((ML['stock']['ru'], ML['stock']['en'], ML['stock']['zh'], ML['stock']['hy']), _row_value(row, 'Stock #')),
    ]
    data = [[_ml_label_cell(*labels, st), Paragraph(_safe(value), st['tbl_val'])] for labels, value in rows]
    table = Table(data, colWidths=[58*mm, 102*mm], hAlign='CENTER')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E5E7EB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 2.4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.4),
    ]))
    return table


def _risk_label(value):
    if value in [True, 'True', 'YES', 'Yes', 'yes', 1]:
        return 'Yes'
    if value in [False, 'False', 'NO', 'No', 'no', 0]:
        return 'No'
    return _safe(value)


def create_single_stone_pdf(row, language='MULTI'):
    """Four-language KURGIN PDF report.

    Language order: Russian, English, Chinese, Armenian.
    The official KURGIN Score and formula are not changed.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm, topMargin=10*mm, bottomMargin=13*mm, title='KURGIN Diamond Analysis Report')
    st = _styles()
    story = []

    logo = _get_logo_path()
    if logo:
        story.append(Image(logo, width=24*mm, height=24*mm, hAlign='CENTER'))
    else:
        story.append(Paragraph('KURGIN', st['brand']))

    story.append(Paragraph(ML['title']['ru'], st['title_ru']))
    story.append(Paragraph(ML['title']['en'], st['title_en']))
    story.append(Paragraph(ML['title']['zh'], st['title_zh']))
    story.append(Paragraph(ML['title']['hy'], st['title_hy']))
    story.append(_identity_card(row, st))
    story.append(Spacer(1, 3))

    score = _score(_row_value(row, 'Kurgin Score'))
    verdict = _safe(_row_value(row, 'Verdict Local', 'Verdict'))
    score_class = _safe(_row_value(row, 'score_band_label_ru', 'score_band_label_en'))
    tags = _safe(_row_value(row, 'tags_all', 'Tags Local', 'Tags'), '')

    story.append(Paragraph(score, st['score']))
    story.append(Paragraph('KURGIN Score / 100', st['muted_center']))
    story.append(Paragraph(f'<b>{verdict}</b>', st['center']))
    story.append(Paragraph(f'<b>Class / Класс:</b> {score_class}', st['center']))
    if tags:
        story.append(Paragraph(f'<b>Tags / Теги:</b> {tags}', st['center']))

    _ml_heading(story, 'short', st)
    story.append(Paragraph(_safe(_row_value(row, 'interpretation_short_ru')), st['body_ru']))
    story.append(Paragraph(_safe(_row_value(row, 'interpretation_short_en')), st['body_en']))
    story.append(Paragraph(_zh_summary(row), st['body_zh']))
    story.append(Paragraph(_hy_summary(row), st['body_hy']))

    _ml_heading(story, 'recommendation', st)
    story.append(Paragraph(_safe(_row_value(row, 'recommendation_ru')), st['body_ru']))
    story.append(Paragraph(_safe(_row_value(row, 'recommendation_en')), st['body_en']))
    story.append(Paragraph(RECOMMENDATION_TEXT['zh'], st['body_zh']))
    story.append(Paragraph(RECOMMENDATION_TEXT['hy'], st['body_hy']))
    story.append(PageBreak())

    _ml_heading(story, 'certificate_geometry', st)
    cert_rows = [
        (('Огранка', 'Shape', '形状', 'Ձև'), _row_value(row, 'Shape')),
        (('Вес', 'Weight', '重量', 'Քաշ'), _row_value(row, 'Weight')),
        (('Цвет', 'Color', '颜色', 'Գույն'), _row_value(row, 'Color')),
        (('Чистота', 'Clarity', '净度', 'Մաքրություն'), _row_value(row, 'Clarity')),
        (('Огранка/полировка/симметрия', 'Cut/Polish/Symmetry', '切工/抛光/对称', 'Կտրում/փայլ/սիմետրիա'), f"{_safe(_row_value(row, 'Cut'))} / {_safe(_row_value(row, 'Polish'))} / {_safe(_row_value(row, 'Symmetry'))}"),
        (('Флуоресценция', 'Fluorescence', '荧光', 'Ֆլուորեսցենցիա'), _row_value(row, 'Fluorescence', 'Fluorescence Intensity')),
        (('Размеры', 'Measurements', '尺寸', 'Չափեր'), _row_value(row, 'Measurements')),
    ]
    geom_rows = [
        (('Площадка / глубина', 'Table / Depth', '台面/深度', 'Սեղան/խորություն'), f"{_safe(_row_value(row, 'TablePercent'))} / {_safe(_row_value(row, 'DepthPercent'))}"),
        (('Корона: угол / %', 'Crown angle / %', '冠部角/比例', 'Պսակի անկյուն/%'), f"{_safe(_row_value(row, 'CrownAngle'))} / {_safe(_row_value(row, 'CrownPercent'))}"),
        (('Павильон: угол / %', 'Pavilion angle / %', '亭部角/比例', 'Պավիլիոնի անկյուն/%'), f"{_safe(_row_value(row, 'PavilionAngle'))} / {_safe(_row_value(row, 'PavilionPercent'))}"),
        (('Рундист %', 'Girdle %', '腰棱比例', 'Գոտու %'), _row_value(row, 'GirdlePercent')),
        (('Мин./макс. диаметр', 'Min/max diameter', '最小/最大直径', 'Նվազ./առավ. տրամագիծ'), f"{_safe(_row_value(row, 'MinDiameter'))} / {_safe(_row_value(row, 'MaxDiameter'))}"),
        (('Средний диаметр', 'Average diameter', '平均直径', 'Միջին տրամագիծ'), _row_value(row, 'AvgDiameter')),
        (('Высота mm', 'Depth mm', '高度 mm', 'Բարձրություն mm'), _row_value(row, 'DepthMM')),
        (('Spread delta %', 'Spread delta %', '视觉尺寸差 %', 'Spread տարբերություն %'), _row_value(row, 'SpreadDelta %')),
        (('Визуальный размер', 'Visual spread', '视觉尺寸', 'Տեսողական չափ'), _row_value(row, 'VisualSpreadStatus')),
        (('Симметрия диаметра', 'Diameter symmetry', '直径对称性', 'Տրամագծի սիմետրիա'), _row_value(row, 'DiameterSymmetryStatus')),
    ]
    story.append(_two_col(cert_rows, geom_rows))
    story.append(PageBreak())

    _ml_heading(story, 'analysis_risks', st)
    analysis_rows = [
        (('KURGIN Score', 'KURGIN Score', 'KURGIN 分数', 'KURGIN միավոր'), score),
        (('Класс', 'Class', '等级', 'Դաս'), score_class),
        (('Triple Score', 'Triple Score', 'Triple 分数', 'Triple միավոր'), _row_value(row, 'Triple Score')),
        (('Structure Modifier', 'Structure Modifier', '结构修正', 'Կառուցվածքային գործակից'), _row_value(row, 'Structure Modifier')),
        (('Visual Check', 'Visual Check', '视觉检查', 'Տեսողական ստուգում'), _risk_label(_row_value(row, 'Visual Check'))),
        (('Critical Risk', 'Critical Risk', '关键风险', 'Կրիտիկական ռիսկ'), _risk_label(_row_value(row, 'Critical Risk'))),
        (('Полнота данных', 'Data completeness', '数据完整度', 'Տվյալների ամբողջականություն'), _row_value(row, 'Data Completeness %')),
        (('Качество отчёта', 'Report quality', '报告质量', 'Հաշվետվության որակ'), _row_value(row, 'Report Quality Status')),
        (('Adjusted preview', 'Adjusted preview', '调整预览', 'Ճշգրտված preview'), _row_value(row, 'AdjustedKURGINScorePreview')),
        (('Diameter policy', 'Diameter policy', '直径策略', 'Տրամագծի քաղաքականություն'), _row_value(row, 'Diameter Policy Status')),
    ]
    risk_rows = [
        (('Nailhead', 'Nailhead', '黑心风险', 'Nailhead'), _row_value(row, 'Nailhead')),
        (('Fisheye', 'Fisheye', '鱼眼风险', 'Fisheye'), _row_value(row, 'Fisheye')),
        (('Fire Loss', 'Fire Loss', '火彩损失', 'Կրակի կորուստ'), _row_value(row, 'Fire Loss')),
        (('Depth Dev', 'Depth Dev', '深度偏差', 'Խորության շեղում'), _row_value(row, 'Depth Dev')),
        (('Crown Dev', 'Crown Dev', '冠部偏差', 'Պսակի շեղում'), _row_value(row, 'Crown Dev')),
        (('Pavilion Dev', 'Pavilion Dev', '亭部偏差', 'Պավիլիոնի շեղում'), _row_value(row, 'Pavilion Dev')),
        (('Balance Err', 'Balance Err', '平衡误差', 'Հավասարակշռության սխալ'), _row_value(row, 'Balance Err')),
        (('Girdle Penalty', 'Girdle Penalty', '腰棱扣分', 'Գոտու տուգանք'), _row_value(row, 'Girdle Penalty')),
        (('Источник размеров', 'Measurement source', '尺寸来源', 'Չափերի աղբյուր'), _row_value(row, 'Chosen Measurement Source', 'Measurement Source')),
        (('Measurement warning', 'Measurement warning', '尺寸警告', 'Չափերի նախազգուշացում'), _row_value(row, 'Measurement Warning')),
    ]
    story.append(_two_col(analysis_rows, risk_rows))
    story.append(PageBreak())

    _ml_heading(story, 'interpretation', st)
    story.append(Paragraph(_safe(_row_value(row, 'interpretation_detail_ru')), st['body_ru']))
    story.append(Paragraph(_safe(_row_value(row, 'interpretation_detail_en')), st['body_en']))
    story.append(Paragraph(_zh_summary(row), st['body_zh']))
    story.append(Paragraph(_hy_summary(row), st['body_hy']))

    warning = _safe(_row_value(row, 'warning_ru'), '')
    if warning:
        story.append(Paragraph('Предупреждение', st['h2_ru']))
        story.append(Paragraph('Warning', st['h2_en']))
        story.append(Paragraph('警告', st['h2_zh']))
        story.append(Paragraph('Նախազգուշացում', st['h2_hy']))
        story.append(Paragraph(warning, st['body_ru']))
        story.append(Paragraph(_safe(_row_value(row, 'warning_en')), st['body_en']))

    _ml_heading(story, 'disclaimer', st)
    story.append(Paragraph(DISCLAIMER_TEXT['ru'], st['small_ru']))
    story.append(Paragraph(DISCLAIMER_TEXT['en'], st['small_en']))
    story.append(Paragraph(DISCLAIMER_TEXT['zh'], st['small_zh']))
    story.append(Paragraph(DISCLAIMER_TEXT['hy'], st['small_hy']))

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()
