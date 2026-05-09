import os
from datetime import datetime

import pandas as pd
import streamlit as st

from access_control.access_manager import ROLES, REPORT_LEVELS, load_access_settings, get_allowed_levels
from excel_tools import create_excel_output, make_analytics, process_dataframe, process_single_stone
from formula_client.engine_client import get_formula_mode
from report_templates.report_columns import filter_report_dataframe

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
        "cloud_ready": "Formula API: подготовлено",
        "formula_mode": "Режим формулы",
        "analytics": "Аналитика",
        "top_stones": "Лучшие камни",
        "risks": "Риски",
        "raw_data": "Данные",
        "download": "Скачать",
        "total": "Всего",
        "success": "Рассчитано",
        "errors": "Ошибки",
        "avg": "Средний Score",
        "manual_calculate": "Рассчитать бриллиант",
        "select_action": "Выберите уровень результата",
        "not_ready_pdf": "PDF/сертификат будет подключён отдельным этапом. Сейчас доступен табличный отчёт.",
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
        "cloud_ready": "Formula API: ready",
        "formula_mode": "Formula mode",
        "analytics": "Analytics",
        "top_stones": "Top Stones",
        "risks": "Risks",
        "raw_data": "Data",
        "download": "Download",
        "total": "Total",
        "success": "Calculated",
        "errors": "Errors",
        "avg": "Average Score",
        "manual_calculate": "Calculate diamond",
        "select_action": "Choose result level",
        "not_ready_pdf": "PDF/certificate export will be added separately. Table reports are available now.",
        "ocr_later": "OCR for photo/PDF will be connected after secure formula API extraction.",
    },
}

LEVEL_TO_REPORT = {
    "score": "Score Only",
    "short": "Short Report",
    "detailed": "Detailed Report",
    "full": "Full Report",
    "professional": "Professional Report",
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
    settings = load_access_settings()
    return report_level in get_allowed_levels(role, settings)


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
    st.markdown(f"### {t['choose_mode']}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="kg-card dark"><h3>◇ {t['single_mode']}</h3><div class="kg-muted">{t['single_desc']}</div></div>""", unsafe_allow_html=True)
        if st.button(t["single_mode"], use_container_width=True):
            st.session_state.mode = "single"
            st.rerun()
    with c2:
        st.markdown(f"""<div class="kg-card green"><h3>▦ {t['pro_mode']}</h3><div class="kg-muted">{t['pro_desc']}</div></div>""", unsafe_allow_html=True)
        if st.button(t["pro_mode"], use_container_width=True):
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
    if level == "pdf":
        st.info(t["not_ready_pdf"])
        return False
    report_level = LEVEL_TO_REPORT[level]
    if not allowed(role, report_level):
        msg = t["locked_registered"] if report_level in ["Short Report", "Detailed Report"] else t["locked_pro"]
        st.markdown(f"<div class='kg-lock'>🔒 {msg}</div>", unsafe_allow_html=True)
        return False
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
    st.dataframe(filter_report_dataframe(pd.DataFrame([stone]), report_level), use_container_width=True, hide_index=True)
    if report_level in ["Full Report", "Professional Report"] and "Breakdown" in stone:
        with st.expander("Breakdown / Разбор"):
            st.text(stone["Breakdown"])


def single_mode(t, language, role):
    if st.button("← " + t["home"]):
        st.session_state.mode = "home"
        st.rerun()
    st.markdown(f"## {t['single_mode']}")
    st.caption(t["single_desc"])

    tab1, tab2, tab3 = st.tabs([t["upload_cert"], t["take_photo"], t["manual_input"]])
    with tab1:
        cert = st.file_uploader(t["upload_cert"], type=["pdf", "jpg", "jpeg", "png"], key="cert_upload")
        st.info(t["ocr_later"])
        if cert is not None and not cert.name.lower().endswith(".pdf"):
            st.image(cert, caption="Certificate preview", use_container_width=True)
    with tab2:
        cam = st.camera_input(t["take_photo"], key="cert_camera")
        if cam is not None:
            st.image(cam, caption="Certificate photo", use_container_width=True)
            st.info(t["ocr_later"])
    with tab3:
        with st.form("manual_form"):
            report = st.text_input("Report #", value="Manual")
            shape = st.selectbox("Shape", ["ROUND", "OVAL", "PEAR", "CUSHION", "EMERALD", "RADIANT", "PRINCESS"])
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
            submitted = st.form_submit_button(t["manual_calculate"], use_container_width=True)
        if submitted:
            params = {
                "Report #": report or "Manual",
                "Shape": shape,
                "CrownAngle": crown_angle,
                "PavilionAngle": pavilion_angle,
                "TablePercent": table_percent,
                "DepthPercent": depth_percent,
                "CrownPercent": crown_percent,
                "PavilionPercent": pavilion_percent,
                "GirdlePercent": girdle_percent,
                "language": language,
            }
            st.session_state.single_result = process_single_stone(params)

    action_buttons(t, "single")
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
        df, missing, mapping_df = process_dataframe(raw_df, language=language)
        if missing:
            st.error("Missing required columns / Не хватает обязательных колонок")
            st.write(missing)
        else:
            st.session_state.batch_df = df
            st.session_state.mapping_df = mapping_df
            st.session_state.batch_analytics = make_analytics(df)

    action_buttons(t, "pro")
    df = st.session_state.batch_df
    analytics = st.session_state.batch_analytics
    if df is None or analytics is None:
        st.info(t["upload_to_continue"])
        return
    active = st.session_state.active_level
    if not gated_level_message(t, role, active):
        return
    report_level = LEVEL_TO_REPORT[active]
    metric_row(t, analytics)
    tabs = st.tabs([t["analytics"], t["top_stones"], t["risks"], t["raw_data"], t["download"]])
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(analytics["verdict_counts"], use_container_width=True, hide_index=True)
        with c2:
            st.dataframe(analytics["score_ranges"], use_container_width=True, hide_index=True)
    with tabs[1]:
        st.dataframe(filter_report_dataframe(analytics["top_10"], report_level), use_container_width=True, hide_index=True)
        st.dataframe(filter_report_dataframe(analytics["worst_10"], report_level), use_container_width=True, hide_index=True)
    with tabs[2]:
        st.dataframe(filter_report_dataframe(analytics["risk_df"], report_level), use_container_width=True, hide_index=True)
    with tabs[3]:
        st.dataframe(filter_report_dataframe(df, report_level), use_container_width=True, hide_index=True)
    with tabs[4]:
        data = create_excel_output(df, analytics, mapping_df=st.session_state.mapping_df, report_level=report_level)
        st.download_button(t["download"], data=data, file_name="kurgin_score_result.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)


def profile_mode(t, role):
    st.markdown(f"## {t['profile']}")
    st.write({"role": role, "formula_mode": get_formula_mode(), "timestamp": datetime.utcnow().isoformat()})


def main():
    init_state()
    language = st.sidebar.selectbox("Language / Язык", ["RU", "EN"], index=0)
    t = TEXT[language]
    role = st.sidebar.selectbox(t["role"], ROLES, index=0)
    st.sidebar.caption("MVP access simulation. Next: real auth/payment.")
    hero(t)

    if st.session_state.mode == "home":
        mode_selector(t)
    elif st.session_state.mode == "single":
        single_mode(t, language, role)
    elif st.session_state.mode == "pro":
        pro_mode(t, language, role)
    elif st.session_state.mode == "profile":
        profile_mode(t, role)

    bottom_nav(t)


if __name__ == "__main__":
    main()
