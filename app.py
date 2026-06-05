import os
from datetime import datetime

import pandas as pd
import streamlit as st

from access_control.access_manager import ROLES, REPORT_LEVELS, load_access_settings, get_allowed_levels
from excel_tools import create_excel_output, make_analytics, process_dataframe, process_single_stone
from formula_client.engine_client import get_formula_mode
from formula_modules.interpretation.interpretation_engine import get_tag_interpretations
from report_templates.report_columns import filter_report_dataframe
from report_templates.pdf_single_stone_report import create_single_stone_pdf

st.set_page_config(
    page_title="Kurgin Score Analyzer",
    page_icon="◇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TEXT = {
    "RU": {
        "app_title": "Kurgin Score",
        "app_subtitle": "Анализ световой архитектуры бриллианта",
        "choose_mode": "Выберите режим",
        "single_mode": "Анализ бриллианта",
        "single_desc": "Один камень: фото, PDF сертификата или ручной ввод параметров.",
        "pro_mode": "Профессиональная аналитика",
        "pro_desc": "Массовая обработка Excel, аналитика коллекции и экспорт отчётов.",
        "score_only": "Получить коэффициент",
        "short": "Краткий отчёт",
        "detailed": "Детальный анализ",
        "full": "Полный отчёт",
        "professional": "Профессиональный обзор",
        "pdf": "PDF / сертификат",
        "locked_registered": "Этот уровень доступен после регистрации.",
        "locked_pro": "Этот уровень доступен для профессионального доступа.",
        "upload_cert": "Загрузить сертификат",
        "take_photo": "Сфотографировать",
        "manual_input": "Ручной ввод",
        "upload_excel": "Загрузить Excel файл",
        "excel_hint": "Поддерживаются .xlsx и .xls. Для стабильной работы используйте таблицу с параметрами сертификата.",
        "result_example": "Результат",
        "upload_to_continue": "Загрузите данные, чтобы получить отчёт.",
        "report_level": "Уровень результата",
        "role": "Доступ",
        "language": "Язык",
        "home": "Главная",
        "diamond": "Камень",
        "pro": "Pro",
        "reports": "Отчёты",
        "profile": "Профиль",
        "nav_hint": "Быстрая навигация",
        "saved_reports": "Сохранённые результаты",
        "single_saved": "Результат анализа бриллианта",
        "batch_saved": "Профессиональная аналитика",
        "no_saved": "Пока нет сохранённых результатов. Выполните анализ бриллианта или загрузите Excel.",
        "interpretations": "Интерпретации",
        "registration_type": "Тип регистрации",
        "buyer": "Покупатель",
        "jeweler_designer": "Ювелир / дизайнер украшений",
        "gemologist": "Геммолог / эксперт",
        "company_partner": "Компания / партнёр",
        "cloud_ready": "Formula API: подготовлено",
        "formula_mode": "Режим формулы",
        "analytics": "Аналитика",
        "top_stones": "Лучшие камни",
        "risks": "Риски",
        "raw_data": "Данные",
        "download": "Скачать",
        "download_excel": "Скачать Excel",
        "download_package": "Скачать полный пакет Excel + PDF",
        "download_package_top": "Скачать Excel + PDF для TOP камней",
        "download_package_all": "Скачать Excel + PDF для всех рассчитанных",
        "total": "Всего",
        "success": "Рассчитано",
        "errors": "Ошибки",
        "avg": "Средний Score",
        "manual_calculate": "Рассчитать бриллиант",
        "select_action": "Выберите уровень результата",
        "pdf_ready": "PDF-отчёт готов к скачиванию.",
        "ocr_later": "OCR для фото/PDF будет подключён после выноса формулы в закрытый API.",
    },
    "EN": {
        "app_title": "Kurgin Score",
        "app_subtitle": "Diamond light architecture analysis",
        "choose_mode": "Choose mode",
        "single_mode": "Diamond Analysis",
        "single_desc": "One stone: photo, PDF certificate or manual parameter input.",
        "pro_mode": "Professional Analytics",
        "pro_desc": "Batch Excel processing, collection analytics and report export.",
        "score_only": "Get Score",
        "short": "Short Report",
        "detailed": "Detailed Analysis",
        "full": "Full Report",
        "professional": "Professional Review",
        "pdf": "PDF / Certificate",
        "locked_registered": "This level is available after registration.",
        "locked_pro": "This level is available for professional access.",
        "upload_cert": "Upload certificate",
        "take_photo": "Take photo",
        "manual_input": "Manual input",
        "upload_excel": "Upload Excel file",
        "excel_hint": "Supports .xlsx and .xls. Use a certificate-parameter table for best stability.",
        "result_example": "Result",
        "upload_to_continue": "Upload data to get a report.",
        "report_level": "Result level",
        "role": "Access",
        "language": "Language",
        "home": "Home",
        "diamond": "Stone",
        "pro": "Pro",
        "reports": "Reports",
        "profile": "Profile",
        "nav_hint": "Quick navigation",
        "saved_reports": "Saved results",
        "single_saved": "Diamond analysis result",
        "batch_saved": "Professional analytics",
        "no_saved": "No saved results yet. Run diamond analysis or upload Excel.",
        "interpretations": "Interpretations",
        "registration_type": "Registration type",
        "buyer": "Buyer",
        "jeweler_designer": "Jeweler / jewelry designer",
        "gemologist": "Gemologist / expert",
        "company_partner": "Company / partner",
        "cloud_ready": "Formula API: ready",
        "formula_mode": "Formula mode",
        "analytics": "Analytics",
        "top_stones": "Top Stones",
        "risks": "Risks",
        "raw_data": "Data",
        "download": "Download",
        "download_excel": "Download Excel",
        "download_package": "Download full Excel + PDF package",
        "download_package_top": "Download Excel + PDF for TOP stones",
        "download_package_all": "Download Excel + PDF for all calculated stones",
        "total": "Total",
        "success": "Calculated",
        "errors": "Errors",
        "avg": "Average Score",
        "manual_calculate": "Calculate diamond",
        "select_action": "Choose result level",
        "pdf_ready": "PDF report is ready for download.",
        "ocr_later": "OCR for photo/PDF will be connected after secure formula API extraction.",
    },
}

LEVEL_TO_REPORT = {
    "score": "Score Only",
    "short": "Short Report",
    "detailed": "Detailed Report",
    "full": "Full Report",
    "professional": "Professional Report",
    "pdf": "Full Report",
}

CSS = """
<style>
:root { --navy:#0b1220; --blue:#13233d; --gold:#d6b46d; --muted:#64748b; --green:#16a34a; }
.main .block-container { max-width: 980px; padding-top: 1rem; padding-bottom: 6rem; }
[data-testid="stSidebar"] { background:#f8fafc; }
.kg-hero { border-radius: 28px; padding: 26px 22px; margin: 8px 0 18px; color:white; background: radial-gradient(circle at top left, #213b67 0%, #0b1220 50%, #070b12 100%); box-shadow:0 18px 45px rgba(15,23,42,.18); }
.kg-brand { font-family: Georgia, 'Times New Roman', serif; letter-spacing:.16em; font-size: clamp(34px, 9vw, 58px); line-height:1; margin-bottom:10px; }
.kg-sub { color:#cbd5e1; letter-spacing:.06em; text-transform:uppercase; font-size: clamp(12px, 3vw, 15px); }
.kg-badge { display:inline-block; margin-top:16px; padding:8px 12px; border:1px solid rgba(214,180,109,.45); border-radius:999px; color:#f8e8bd; font-size:13px; }
.kg-card { border:1px solid #e5e7eb; border-radius:22px; padding:18px; background:white; box-shadow:0 10px 30px rgba(15,23,42,.06); margin-bottom:14px; }
.kg-card.dark { background:linear-gradient(135deg,#111827,#172033); color:white; border-color:#334155; }
.kg-card.green { background:linear-gradient(135deg,#082f22,#123b2e); color:white; border-color:#22543d; }
.kg-card h3 { margin:0 0 8px 0; font-size:22px; }
.kg-muted { color:#64748b; font-size:14px; }
.kg-card.dark .kg-muted, .kg-card.green .kg-muted { color:#cbd5e1; }
.kg-score { font-family: Georgia, 'Times New Roman', serif; font-size:64px; color:var(--gold); line-height:1; }
.kg-verdict { display:inline-block; padding:8px 12px; border-radius:999px; background:#ecfdf5; color:#166534; font-weight:700; margin-top:8px; }
.kg-lock { padding:15px; background:#fff7ed; border:1px solid #fed7aa; border-radius:18px; color:#9a3412; margin-top:12px; }
.kg-bottom-nav { position: fixed; left: 50%; transform: translateX(-50%); bottom: 12px; z-index: 999; width: min(560px, calc(100% - 24px)); display:flex; justify-content:space-around; gap:8px; padding:10px; border-radius:24px; background:rgba(11,18,32,.92); backdrop-filter: blur(12px); box-shadow:0 12px 40px rgba(15,23,42,.28); }
.kg-bottom-nav span { color:#e5e7eb; font-size:12px; text-align:center; }
.stButton > button { border-radius:14px; min-height:46px; font-weight:700; border:1px solid #cbd5e1; }
.stDownloadButton > button { border-radius:14px; min-height:46px; font-weight:700; }
@media (max-width: 720px) { .main .block-container { padding-left: 14px; padding-right: 14px; } .kg-card { padding:15px; } div[data-testid="column"] { width:100% !important; flex: 1 1 100% !important; } .kg-score { font-size:56px; } }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


def init_state():
    st.session_state.setdefault("mode", "home")
    st.session_state.setdefault("single_result", None)
    st.session_state.setdefault("batch_df", None)
    st.session_state.setdefault("batch_analytics", None)
    st.session_state.setdefault("mapping_df", None)
    st.session_state.setdefault("active_level", "score")


def allowed(role, report_level):
    # Open access mode for current formula/report development stage.
    # Real roles, payments and access gates will be moved to Admin/Auth layer later.
    return True


def score_label(score):
    if pd.isna(score):
        return "—"
    try:
        return f"{float(score):.2f}"
    except Exception:
        return str(score)


def hero(t):
    mode = get_formula_mode()
    st.markdown(
        f"""
        <div class="kg-hero">
            <div class="kg-brand">KURGIN SCORE</div>
            <div class="kg-sub">{t['app_subtitle']}</div>
            <div class="kg-badge">{t['cloud_ready']} · {t['formula_mode']}: {mode}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bottom_nav(t):
    st.markdown(f"#### {t['nav_hint']}")
    cols = st.columns(5)
    nav_items = [
        ("home", "⌂", t["home"]),
        ("single", "◇", t["diamond"]),
        ("pro", "▦", t["pro"]),
        ("reports", "▤", t["reports"]),
        ("profile", "○", t["profile"]),
    ]
    for col, (mode, icon, label) in zip(cols, nav_items):
        with col:
            if st.button(f"{icon}\n{label}", key=f"nav_{mode}", use_container_width=True):
                st.session_state.mode = mode
                st.rerun()

    st.markdown(
        f"""
        <div class="kg-bottom-nav">
            <span>⌂<br>{t['home']}</span>
            <span>◇<br>{t['diamond']}</span>
            <span>▦<br>{t['pro']}</span>
            <span>▤<br>{t['reports']}</span>
            <span>○<br>{t['profile']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mode_selector(t):
    st.markdown("### Основные сценарии")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            "<div class='kg-card dark'><h3>◇ KURGIN Score 1 камня</h3>"
            "<div class='kg-muted'>Быстрый расчёт коэффициента по параметрам камня.</div></div>",
            unsafe_allow_html=True,
        )
        if st.button("KURGIN Score 1 камня", key="mode_single_score", use_container_width=True):
            st.session_state.active_level = "score"
            st.session_state.mode = "single"
            st.rerun()

    with c2:
        st.markdown(
            "<div class='kg-card dark'><h3>◇ Полный анализ 1 камня</h3>"
            "<div class='kg-muted'>Полный разбор одного камня по введённым параметрам.</div></div>",
            unsafe_allow_html=True,
        )
        if st.button("Полный анализ 1 камня", key="mode_single_full", use_container_width=True):
            st.session_state.active_level = "full"
            st.session_state.mode = "single"
            st.rerun()

    with c3:
        st.markdown(
            "<div class='kg-card green'><h3>▦ Excel-анализ</h3>"
            "<div class='kg-muted'>Загрузил Excel → увидел результат → скачал Excel.</div></div>",
            unsafe_allow_html=True,
        )
        if st.button("Загрузить Excel", key="mode_excel", use_container_width=True):
            st.session_state.active_level = "professional"
            st.session_state.mode = "pro"
            st.rerun()


def action_buttons(t, prefix="single"):
    st.markdown(f"#### {t['select_action']}")
    actions = [
        ("score", t["score_only"]),
        ("short", t["short"]),
        ("detailed", t["detailed"]),
        ("full", t["full"]),
        ("professional", t["professional"]),
        ("pdf", t["pdf"]),
    ]
    cols = st.columns(2)
    for i, (key, label) in enumerate(actions):
        with cols[i % 2]:
            if st.button(label, key=f"{prefix}_{key}", use_container_width=True):
                st.session_state.active_level = key


def gated_level_message(t, role, level):
    # All report levels are temporarily open while the formula/report logic is being finalized.
    return True


def render_single_result(t, role):
    stone = st.session_state.single_result
    if stone is None:
        st.info(t["upload_to_continue"])
        return
    active = st.session_state.active_level
    if not gated_level_message(t, role, active):
        return
    report_level = LEVEL_TO_REPORT[active]
    st.markdown("<div class='kg-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='kg-score'>{score_label(stone['Kurgin Score'])}</div>", unsafe_allow_html=True)
    verdict = stone.get("Verdict Local", stone.get("Verdict", "—"))
    st.markdown(f"<div class='kg-verdict'>{verdict}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if active == "pdf":
        pdf_data = create_single_stone_pdf(stone, language="MULTI")
        title = str(stone.get("Stone Title", "kurgin_report")).replace(" ", "_").replace("/", "_")
        st.success(t.get("pdf_ready", "PDF report is ready."))
        st.download_button(
            label="Скачать PDF / Download PDF",
            data=pdf_data,
            file_name=f"{title}_KURGIN_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
            on_click="ignore",
        )

    st.dataframe(filter_report_dataframe(pd.DataFrame([stone]), report_level), use_container_width=True, hide_index=True)

    raw_tags = [tag.strip() for tag in str(stone.get("Tags", "")).split(",") if tag.strip()]
    tag_interpretations = get_tag_interpretations(raw_tags, language="RU" if "ОТКЛОНЕНО" in str(stone.get("Verdict Local", "")) or "ТОП" in str(stone.get("Verdict Local", "")) else "EN")
    if tag_interpretations and report_level in ["Short Report", "Detailed Report", "Full Report", "Professional Report"]:
        with st.expander(t["interpretations"], expanded=True):
            st.dataframe(pd.DataFrame(tag_interpretations), use_container_width=True, hide_index=True)

    if report_level in ["Full Report", "Professional Report"] and "Breakdown" in stone:
        with st.expander("Breakdown / Разбор"):
            st.text(stone["Breakdown"])


def single_mode(t, language, role):
    if st.button("← " + t["home"]):
        st.session_state.mode = "home"
        st.rerun()
    if st.session_state.active_level not in ["score", "full"]:
        st.session_state.active_level = "score"

    single_title = "KURGIN Score 1 камня" if st.session_state.active_level == "score" else "Полный анализ 1 камня"
    st.markdown(f"## {single_title}")
    st.caption("Ручной ввод параметров камня.")
    tab3 = st.container()
    with tab3:
        with st.form("manual_form"):
            st.markdown("### Основные данные камня")
            c0a, c0b, c0c = st.columns(3)
            stock = c0a.text_input("Stock #", value="")
            report = c0b.text_input("Report #", value="Manual")
            lab = c0c.text_input("Lab", value="IGI")

            c0d, c0e, c0f, c0g = st.columns(4)
            shape = c0d.selectbox("Shape", ["ROUND", "OVAL", "PEAR", "CUSHION", "EMERALD", "RADIANT", "PRINCESS"])
            weight = c0e.text_input("Weight", value="")
            color = c0f.text_input("Color", value="")
            clarity = c0g.text_input("Clarity", value="")

            c0h, c0i, c0j = st.columns(3)
            cut = c0h.text_input("Cut", value="")
            polish = c0i.text_input("Polish", value="")
            symmetry = c0j.text_input("Symmetry", value="")

            c0k, c0l = st.columns(2)
            fluorescence_intensity = c0k.text_input("Fluorescence Intensity", value="")
            fluorescence_color = c0l.text_input("Fluorescence Color", value="")

            measurements = st.text_input("Measurements", value="", help="Например: 6.360x6.400x3.970")

            with st.expander("Дополнительные данные сертификата", expanded=False):
                cA, cB, cC = st.columns(3)
                availability = cA.text_input("Availability", value="")
                location = cB.text_input("Location", value="")
                treatment = cC.text_input("Treatment", value="")

                cD, cE, cF = st.columns(3)
                growth_method = cD.text_input("Growth Method", value="")
                diamond_type = cE.text_input("Diamond Type", value="")
                inscription = cF.text_input("Inscription", value="")

                cert_comment = st.text_area("Cert comment", value="", height=80)
                cert_file = st.text_input("CertFile", value="")

            with st.expander("Визуальные признаки и включения", expanded=False):
                cV1, cV2, cV3, cV4 = st.columns(4)
                shade = cV1.text_input("Shade", value="")
                milky = cV2.text_input("Milky", value="")
                eye_clean = cV3.text_input("Eye Clean", value="")
                bgm = cV4.text_input("BGM", value="")

                key_to_symbols = st.text_input("KeyToSymbols", value="")
                cI1, cI2, cI3 = st.columns(3)
                white_inclusion = cI1.text_input("White Inclusion", value="")
                black_inclusion = cI2.text_input("Black Inclusion", value="")
                open_inclusion = cI3.text_input("Open Inclusion", value="")

            st.markdown("### Геометрия и пропорции")
            c1, c2 = st.columns(2)
            crown_angle = c1.number_input("Crown Angle", value=34.5)
            pavilion_angle = c2.number_input("Pavilion Angle", value=40.75)
            c3, c4 = st.columns(2)
            table_percent = c3.number_input("Table %", value=56.0)
            depth_percent = c4.number_input("Depth %", value=61.5)
            c5, c6, c7 = st.columns(3)
            crown_percent = c5.number_input("Crown %", value=15.0)
            pavilion_percent = c6.number_input("Pavilion %", value=43.0)
            girdle_percent = c7.number_input("Girdle %", value=3.5)

            c8, c9, c10, c11 = st.columns(4)
            girdle_thin = c8.text_input("Girdle Thin", value="")
            girdle_thick = c9.text_input("Girdle Thick", value="")
            girdle_condition = c10.text_input("Girdle Condition", value="")
            culet_size = c11.text_input("Culet Size", value="")
            culet_condition = st.text_input("Culet Condition", value="")

            submitted = st.form_submit_button(t["manual_calculate"], use_container_width=True)

        if submitted:
            params = {
                "Stock #": stock,
                "Availability": availability,
                "Report #": report or "Manual",
                "Lab": lab,
                "Shape": shape,
                "Weight": weight,
                "Color": color,
                "Clarity": clarity,
                "Cut": cut,
                "Polish": polish,
                "Symmetry": symmetry,
                "Fluorescence": fluorescence_intensity,
                "Fluorescence Intensity": fluorescence_intensity,
                "Fluorescence Color": fluorescence_color,
                "Measurements": measurements,
                "Location": location,
                "Treatment": treatment,
                "Growth Method": growth_method,
                "Diamond Type": diamond_type,
                "Inscription": inscription,
                "Cert comment": cert_comment,
                "CertFile": cert_file,
                "Shade": shade,
                "Milky": milky,
                "Eye Clean": eye_clean,
                "BGM": bgm,
                "KeyToSymbols": key_to_symbols,
                "White Inclusion": white_inclusion,
                "Black Inclusion": black_inclusion,
                "Open Inclusion": open_inclusion,
                "CrownAngle": crown_angle,
                "PavilionAngle": pavilion_angle,
                "TablePercent": table_percent,
                "DepthPercent": depth_percent,
                "CrownPercent": crown_percent,
                "PavilionPercent": pavilion_percent,
                "GirdlePercent": girdle_percent,
                "GirdleThin": girdle_thin,
                "GirdleThick": girdle_thick,
                "GirdleCondition": girdle_condition,
                "CuletSize": culet_size,
                "CuletCondition": culet_condition,
                "language": language,
            }
            st.session_state.single_result = process_single_stone(params)

    render_single_result(t, role)


def metric_row(t, analytics):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t["total"], analytics["total"])
    c2.metric(t["success"], analytics["successful"])
    c3.metric(t["errors"], analytics["errors"])
    avg = analytics["avg_score"]
    c4.metric(t["avg"], round(avg, 2) if pd.notna(avg) else "—")


def pro_mode(t, language, role):
    if st.button("← " + t["home"]):
        st.session_state.mode = "home"
        st.rerun()
    st.markdown(f"## {t['pro_mode']}")
    st.caption(t["pro_desc"])
    uploaded = st.file_uploader(t["upload_excel"], type=["xlsx", "xls"], help=t["excel_hint"], key="excel_upload")
    if uploaded:
        raw_df = pd.read_excel(uploaded)
        try:
            uploaded.seek(0)
            fluorescence_df = pd.read_excel(uploaded, keep_default_na=False)
            for source_column in fluorescence_df.columns:
                if "fluor" in str(source_column).lower():
                    raw_df[source_column] = fluorescence_df[source_column]
        finally:
            try:
                uploaded.seek(0)
            except Exception:
                pass
        df, missing, mapping_df = process_dataframe(raw_df, language=language)
        if missing:
            st.warning("Missing required columns were converted into Issues / Недостающие колонки перенесены в Issues")
            st.write(missing)
        st.session_state.batch_df = df
        st.session_state.mapping_df = mapping_df
        st.session_state.batch_analytics = make_analytics(df)

        ok_count = int((df.get("Calculation Status", pd.Series(dtype=str)) == "OK").sum())
        issue_count = int((df.get("Calculation Status", pd.Series(dtype=str)) != "OK").sum())
        mapped_count = int((mapping_df["Status"].astype(str) != "not mapped").sum()) if "Status" in mapping_df.columns else 0
        total_cols = len(mapping_df)
        st.success(f"Upload check: {ok_count} ready / {issue_count} issues · Columns recognized: {mapped_count}/{total_cols}")

    df = st.session_state.batch_df
    analytics = st.session_state.batch_analytics
    if df is None or analytics is None:
        st.info(t["upload_to_continue"])
        return

    report_level = "Professional Report"
    metric_row(t, analytics)

    tabs = st.tabs([t["analytics"], t["raw_data"], t["download"]])

    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(analytics["verdict_counts"], use_container_width=True, hide_index=True)
        with c2:
            st.dataframe(analytics["score_ranges"], use_container_width=True, hide_index=True)

    with tabs[1]:
        st.dataframe(filter_report_dataframe(df, report_level), use_container_width=True, hide_index=True)

    with tabs[2]:
        data = create_excel_output(df, analytics, mapping_df=st.session_state.mapping_df, report_level=report_level)
        st.download_button(
            t.get("download_excel", t["download"]),
            data=data,
            file_name="kurgin_score_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            on_click="ignore",
        )


def reports_mode(t, role):
    st.markdown(f"## {t['saved_reports']}")
    has_any = False

    if st.session_state.single_result is not None:
        has_any = True
        st.markdown(f"### {t['single_saved']}")
        stone = st.session_state.single_result
        st.metric("Kurgin Score", score_label(stone.get("Kurgin Score")))
        st.write(stone.get("Verdict Local", stone.get("Verdict", "—")))
        st.dataframe(pd.DataFrame([stone]), use_container_width=True, hide_index=True)

    if st.session_state.batch_df is not None and st.session_state.batch_analytics is not None:
        has_any = True
        st.markdown(f"### {t['batch_saved']}")
        metric_row(t, st.session_state.batch_analytics)
        st.dataframe(st.session_state.batch_analytics["top_10"], use_container_width=True, hide_index=True)

    if not has_any:
        st.info(t["no_saved"])


def profile_mode(t, role):
    st.markdown(f"## {t['profile']}")
    st.selectbox(
        t["registration_type"],
        [t["buyer"], t["jeweler_designer"], t["gemologist"], t["company_partner"]],
        index=0,
    )
    st.write({"access_mode": "open", "formula_mode": get_formula_mode(), "timestamp": datetime.utcnow().isoformat()})


def main():
    init_state()
    language = st.sidebar.selectbox("Language / Язык", ["RU", "EN"], index=0)
    t = TEXT[language]
    role = "Open Access"
    st.sidebar.caption("Доступы временно открыты для разработки формулы и отчётов.")
    hero(t)

    if st.session_state.mode == "home":
        mode_selector(t)
    elif st.session_state.mode == "single":
        single_mode(t, language, role)
    elif st.session_state.mode == "pro":
        pro_mode(t, language, role)
    else:
        st.session_state.mode = "home"
        st.rerun()


if __name__ == "__main__":
    main()
