
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


def _ml_label_cell(ru, en, zh, hy, st):
    return [
        Paragraph(f'<b>{ru}</b>', st['tbl_key']),
        Paragraph(en, st['tbl_key']),
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
    """Compact RU/EN KURGIN PDF report for one stone.

    The official KURGIN Score and formula are not changed.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=12*mm,
        leftMargin=12*mm,
        topMargin=9*mm,
        bottomMargin=12*mm,
        title='KURGIN Diamond Analysis Report',
    )
    st = _styles()
    story = []

    def esc(value):
        if value is None:
            text_value = "—"
        else:
            text_value = str(value).strip()
            if not text_value or text_value.lower() in {"nan", "null"}:
                text_value = "—"
        return (
            str(text_value)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
        )

    def para(value, style='tbl_val'):
        return Paragraph(esc(value), st[style])

    def label(ru, en):
        return Paragraph(f'<b>{esc(ru)}</b><br/><font size="5.8">{esc(en)}</font>', st['tbl_key'])

    def raw_value_from(*names, default='—'):
        for name in names:
            try:
                value = row.get(name)
            except Exception:
                value = None
            if value is None:
                continue
            text_value = str(value).strip()
            if not text_value:
                continue
            if text_value.lower() in {"nan", "null"}:
                continue
            if text_value in {"—", "-"}:
                continue
            return text_value
        return default

    def value_from(*names, default='—'):
        return esc(raw_value_from(*names, default=default))

    def angle(value):
        value = value_from(value) if isinstance(value, str) else esc(value)
        if value == '—':
            return value
        return value if '°' in value else f'{value}°'

    def section(title):
        return [
            Paragraph(f'<b>{esc(title)}</b>', st['center']),
            '',
            '',
        ]

    def cert_ru(text):
        return Paragraph(f'<b>{esc(text)}</b>', st['tbl_key'])

    def cert_en(text):
        return Paragraph(esc(text), st['tbl_key'])

    def certificate_table():
        rows = [
            section('Информация / Information'),
            [cert_ru('Лаборатория'), cert_en('Lab'), para(value_from('Lab'))],
            [cert_ru('Номер сертификата'), cert_en('Report Number'), para(value_from('Report #', 'Report Number'))],
            [cert_ru('Дата отчёта'), cert_en('Report Date'), para(value_from('Report Date'))],
            [cert_ru('Описание'), cert_en('Description'), para(value_from('Description'))],

            section('Детали камня / Stone Details'),
            [cert_ru('Форма и стиль огранки'), cert_en('Shape and Cutting Style'), para(value_from('Shape and Cutting Style', 'Shape'))],
            [cert_ru('Размеры'), cert_en('Measurements'), para(value_from('Measurements'))],
            [cert_ru('Вес в каратах'), cert_en('Carat Weight'), para(value_from('Carat Weight', 'Weight'))],
            [cert_ru('Цвет'), cert_en('Color Grade'), para(value_from('Color Grade', 'Color'))],
            [cert_ru('Чистота'), cert_en('Clarity Grade'), para(value_from('Clarity Grade', 'Clarity'))],

            section('Качество / Quality'),
            [cert_ru('Качество огранки'), cert_en('Cut Grade'), para(value_from('Cut Grade', 'Cut'))],
            [cert_ru('Полировка'), cert_en('Polish'), para(value_from('Polish'))],
            [cert_ru('Симметрия'), cert_en('Symmetry'), para(value_from('Symmetry'))],
            [cert_ru('Флуоресценция'), cert_en('Fluorescence'), para(value_from('Fluorescence', 'Fluorescence Intensity'))],

            section('Геометрия / Geometry'),
            [cert_ru('Глубина %'), cert_en('Depth %'), para(value_from('DepthPercent'))],
            [cert_ru('Таблица %'), cert_en('Table %'), para(value_from('TablePercent'))],
            [cert_ru('Высота короны %'), cert_en('Crown Height %'), para(value_from('CrownPercent'))],
            [cert_ru('Угол короны'), cert_en('Crown Angle'), para(angle('CrownAngle'))],
            [cert_ru('Угол павильона'), cert_en('Pavilion Angle'), para(angle('PavilionAngle'))],
            [cert_ru('Глубина павильона %'), cert_en('Pavilion Depth %'), para(value_from('PavilionPercent'))],
        ]

        table = Table(rows, colWidths=[52*mm, 55*mm, 60*mm], hAlign='CENTER')
        style = [
            ('BOX', (0, 0), (-1, -1), 0.55, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.35, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 1.7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1.7),
        ]

        for idx, row_data in enumerate(rows):
            if len(row_data) == 3 and row_data[1] == '' and row_data[2] == '':
                style.extend([
                    ('SPAN', (0, idx), (2, idx)),
                    ('BACKGROUND', (0, idx), (2, idx), colors.HexColor('#F3F4F6')),
                    ('ALIGN', (0, idx), (2, idx), 'CENTER'),
                    ('TOPPADDING', (0, idx), (2, idx), 2.0),
                    ('BOTTOMPADDING', (0, idx), (2, idx), 2.0),
                ])

        table.setStyle(TableStyle(style))
        return table

    def kurgin_elements_table():
        def status_para(name):
            return para(raw_value_from(name))

        def explanation_para(name):
            return para(raw_value_from(name))

        def tag_note(status_col, explanation_col, inactive_ru):
            status = raw_value_from(status_col, default="")
            if status.startswith("Not calculated"):
                return para("Не рассчитано из-за недостатка данных.")
            if status.startswith("Not triggered"):
                return para(inactive_ru)
            return para(raw_value_from(explanation_col))

        rows = [
            [label('Огонь', 'Fire'), status_para('Fire Profile'), explanation_para('Fire Explanation RU')],
            [label('Блеск', 'Brilliance'), status_para('Brilliance Profile'), explanation_para('Brilliance Explanation RU')],
            [label('Контраст', 'Contrast'), status_para('Contrast Profile'), explanation_para('Contrast Explanation RU')],
            [label('Баланс', 'Balance'), status_para('Balance Profile'), explanation_para('Balance Explanation RU')],

            [
                label('Идеальная сборка', 'Perfect Build'),
                status_para('Perfect Build Status'),
                tag_note('Perfect Build Status', 'Perfect Build Explanation RU', 'Тег идеальной сборки не сработал по текущей модели.'),
            ],
            [
                label('Скрытый вес', 'Hidden Weight'),
                status_para('Hidden Weight Status'),
                tag_note('Hidden Weight Status', 'Hidden Weight Explanation RU', 'Признаки скрытого веса не выявлены по текущей модели.'),
            ],
            [
                label('Риск тёмного центра', 'Nailhead Risk'),
                status_para('Nailhead Risk Status'),
                tag_note('Nailhead Risk Status', 'Nailhead Risk Explanation RU', 'Риск тёмного центра не выявлен по текущей модели.'),
            ],
            [
                label('Риск рыбьего глаза', 'Fisheye Risk'),
                status_para('Fisheye Risk Status'),
                tag_note('Fisheye Risk Status', 'Fisheye Risk Explanation RU', 'Риск эффекта рыбьего глаза не выявлен по текущей модели.'),
            ],
            [
                label('Слабая игра света', 'Low Fire'),
                status_para('Low Fire Status'),
                tag_note('Low Fire Status', 'Low Fire Explanation RU', 'Снижение игры света не выявлено по текущей модели.'),
            ],
        ]

        data = [[
            Paragraph('<b>Элемент / Element</b>', st['tbl_key']),
            Paragraph('<b>Статус / Status</b>', st['tbl_key']),
            Paragraph('<b>Пояснение / Explanation</b>', st['tbl_key']),
        ]] + rows

        table = Table(data, colWidths=[42*mm, 43*mm, 82*mm], hAlign='CENTER', repeatRows=1)
        table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.55, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.30, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F3F4F6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2.5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2.5),
            ('TOPPADDING', (0, 0), (-1, -1), 1.7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1.7),
        ]))
        return table

    logo = _get_logo_path()
    if logo:
        story.append(Image(logo, width=18*mm, height=18*mm, hAlign='CENTER'))
    else:
        story.append(Paragraph('KURGIN', st['brand']))

    story.append(Paragraph(ML['title']['ru'], st['title_ru']))
    story.append(Paragraph(ML['title']['en'], st['title_en']))

    score = _score(_row_value(row, 'Kurgin Score'))

    score_class_ru = raw_value_from('score_band_label_ru', default='')
    score_class_en = raw_value_from('score_band_label_en', default='')
    if score_class_ru and score_class_en and score_class_ru != score_class_en:
        score_class = f"{score_class_ru} / {score_class_en}"
    else:
        score_class = score_class_ru or score_class_en or value_from('Verdict Local', 'Verdict')

    active_tags_raw = raw_value_from('Active KURGIN Tags', 'tags_all', 'Tags Local', 'Tags', default='')
    tag_public_labels = {
        'Perfect Build': 'Идеальная сборка / Perfect Build',
        'Hidden Weight': 'Скрытый вес / Hidden Weight',
        'Nailhead Risk': 'Риск тёмного центра / Nailhead Risk',
        'Fisheye Risk': 'Риск рыбьего глаза / Fisheye Risk',
        'Low Fire': 'Слабая игра света / Low Fire',
    }

    signal_parts = []
    for item in str(active_tags_raw or '').replace(';', ',').split(','):
        item = item.strip()
        if item:
            signal_parts.append(tag_public_labels.get(item, item))
    main_signal = '; '.join(signal_parts)

    story.append(Spacer(1, 1.5))
    story.append(Paragraph(score, st['score']))
    story.append(Paragraph('KURGIN Score / 100', st['muted_center']))
    story.append(Paragraph(f'<b>Класс / Class:</b> {esc(score_class)}', st['center']))
    if main_signal:
        story.append(Paragraph(f'<b>Основной сигнал / Main signal:</b> {esc(main_signal)}', st['center']))

    story.append(Spacer(1, 3))
    story.append(Paragraph('<b>Краткий вывод / Short conclusion</b>', st['h2_ru']))
    story.append(Paragraph(esc(_row_value(row, 'interpretation_short_ru')), st['body_ru']))
    story.append(Paragraph(esc(_row_value(row, 'interpretation_short_en')), st['body_en']))

    story.append(Spacer(1, 2))
    story.append(Paragraph('<b>Рекомендация / Recommendation</b>', st['h2_ru']))
    story.append(Paragraph(esc(_row_value(row, 'recommendation_ru')), st['body_ru']))
    story.append(Paragraph(esc(_row_value(row, 'recommendation_en')), st['body_en']))

    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Данные сертификата / Certificate Data</b>', st['h2_ru']))
    story.append(certificate_table())

    story.append(PageBreak())
    story.append(Paragraph('<b>KURGIN-анализ / KURGIN Analysis</b>', st['h2_ru']))
    story.append(kurgin_elements_table())

    warning = _safe(_row_value(row, 'warning_ru'), '')
    if warning:
        story.append(Spacer(1, 3))
        story.append(Paragraph('<b>Предупреждение / Warning</b>', st['h2_ru']))
        story.append(Paragraph(esc(warning), st['body_ru']))
        story.append(Paragraph(esc(_row_value(row, 'warning_en')), st['body_en']))

    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Ограничение анализа / Disclaimer</b>', st['h2_ru']))
    story.append(Paragraph(esc(DISCLAIMER_TEXT['ru']), st['small_ru']))
    story.append(Paragraph(esc(DISCLAIMER_TEXT['en']), st['small_en']))

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()
