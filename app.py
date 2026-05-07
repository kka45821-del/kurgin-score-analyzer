import streamlit as st
import pandas as pd

from excel_tools import (
    process_dataframe,
    make_analytics,
    create_excel_output,
    process_single_stone,
)
from access_control.access_manager import (
    ROLES,
    REPORT_LEVELS,
    load_access_settings,
    save_access_settings,
    get_allowed_levels,
)
from report_templates.report_columns import filter_report_dataframe


st.set_page_config(
    page_title="Kurgin Score Analyzer",
    layout="wide"
)

TEXT = {
    "RU": {
        "title": "Kurgin Score Analyzer",
        "subtitle": "Инженерный анализ световой архитектуры бриллианта",
        "upload_excel": "Загрузите Excel файл",
        "analytics": "Аналитика",
        "top_stones": "Лучшие камни",
        "risks": "Риски",
        "stone_debug": "Разбор камня",
        "raw_data": "Данные",
        "download": "Скачать",
        "certificate": "Сертификат",
        "access_admin": "Доступ",
        "summary": "Краткая аналитика",
        "all_stones": "Всего камней",
        "success": "Успешно рассчитано",
        "errors": "Ошибок",
        "avg_score": "Средний Score",
        "verdicts": "Распределение по вердиктам",
        "ranges": "Распределение по диапазонам Score",
        "top10": "Топ 10 камней",
        "worst10": "Худшие 10 камней",
        "risk_stones": "Камни с рисками",
        "critical_risk": "Критические риски",
        "debug_select": "Выберите Report #",
        "verdict": "Вердикт",
        "tags": "Теги",
        "risks_title": "Риски",
        "diagnostics": "Диагностика",
        "breakdown": "Разбор",
        "full_data": "Полные данные камня",
        "raw_table": "Исходные и обработанные данные",
        "download_result": "Скачать результат",
        "download_excel": "Скачать обработанный Excel",
        "role": "Роль пользователя",
        "report_level": "Уровень отчёта",
        "score_only_note": "Уровень отчёта управляет тем, какие данные видит пользователь.",
        "certificate_hint": "Сфотографируйте сертификат или загрузите фото. OCR будет добавлен следующим этапом.",
    },
    "EN": {
        "title": "Kurgin Score Analyzer",
        "subtitle": "Engineering analysis of diamond light architecture",
        "upload_excel": "Upload Excel file",
        "analytics": "Analytics",
        "top_stones": "Top Stones",
        "risks": "Risks",
        "stone_debug": "Stone Debug",
        "raw_data": "Raw Data",
        "download": "Download",
        "certificate": "Certificate",
        "access_admin": "Access",
        "summary": "Summary",
        "all_stones": "Total Stones",
        "success": "Calculated",
        "errors": "Errors",
        "avg_score": "Average Score",
        "verdicts": "Verdict Distribution",
        "ranges": "Score Distribution",
        "top10": "Top 10 Stones",
        "worst10": "Worst 10 Stones",
        "risk_stones": "Risk Stones",
        "critical_risk": "Critical Risks",
        "debug_select": "Select Report #",
        "verdict": "Verdict",
        "tags": "Tags",
        "risks_title": "Risks",
        "diagnostics": "Diagnostics",
        "breakdown": "Breakdown",
        "full_data": "Full Stone Data",
        "raw_table": "Raw and Processed Data",
        "download_result": "Download Result",
        "download_excel": "Download Processed Excel",
        "role": "User Role",
        "report_level": "Report Level",
        "score_only_note": "Report level controls what data the user can see.",
        "certificate_hint": "Take a certificate photo or upload an image. OCR will be added in the next stage.",
    },
}

CUSTOM_CSS = """
<style>
    .main .block-container {
        padding-top: 2.2rem;
        padding-bottom: 4rem;
        max-width: 1320px;
    }
    h1 {
        letter-spacing: -0.04em;
        font-size: 3.1rem !important;
        margin-bottom: 0.2rem !important;
    }
    .premium-subtitle {
        font-size: 1.05rem;
        color: #cbd5e1;
        margin-bottom: 1.5rem;
    }
    .hero-card {
        padding: 1.35rem 1.5rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #0b1220 0%, #1f2937 55%, #111827 100%);
        color: white;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.16);
        margin-bottom: 1.2rem;
    }
    .hero-card small { color: #cbd5e1; }
    .metric-card {
        padding: 1rem 1.15rem;
        border-radius: 18px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.055);
    }
    .soft-card {
        padding: 1.2rem;
        border-radius: 20px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        letter-spacing: -0.04em;
    }
    div[data-testid="stTabs"] button { font-weight: 650; }
    [data-testid="stSidebar"] { background: #f8fafc; }
</style>
"""


def score_label(score):
    if pd.isna(score):
        return "—"
    try:
        return f"{float(score):.2f}"
    except Exception:
        return str(score)


def show_hero(t, role, report_level):
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>{t['title']}</h1>
            <div class="premium-subtitle">{t['subtitle']}</div>
            <small>{t['role']}: <b>{role}</b> · {t['report_level']}: <b>{report_level}</b></small>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_metrics(t, analytics):
    col1, col2, col3, col4 = st.columns(4)
    avg_score = analytics["avg_score"]
    metrics = [
        (t["all_stones"], analytics["total"]),
        (t["success"], analytics["successful"]),
        (t["errors"], analytics["errors"]),
        (t["avg_score"], round(avg_score, 2) if pd.notna(avg_score) else "—"),
    ]
    for col, (label, value) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(label, value)
            st.markdown('</div>', unsafe_allow_html=True)


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

language = st.sidebar.selectbox("Language / Язык", ["RU", "EN"])
t = TEXT[language]

access_settings = load_access_settings()
role = st.sidebar.selectbox(t["role"], ROLES, index=0)
allowed_levels = get_allowed_levels(role, access_settings)
report_level = st.sidebar.selectbox(t["report_level"], allowed_levels)
st.sidebar.caption(t["score_only_note"])

show_hero(t, role, report_level)

uploaded_file = st.file_uploader(t["upload_excel"], type=["xlsx"])

df = None
analytics = None
mapping_df = None

if uploaded_file:
    raw_df = pd.read_excel(uploaded_file)
    df, missing_columns, mapping_df = process_dataframe(raw_df, language=language)
    if missing_columns:
        st.error("Missing required columns / Не хватает обязательных колонок")
        st.write(missing_columns)
    else:
        analytics = make_analytics(df)

tabs = st.tabs([
    t["analytics"],
    t["top_stones"],
    t["risks"],
    t["stone_debug"],
    t["certificate"],
    t["raw_data"],
    t["download"],
    t["access_admin"],
])

with tabs[0]:
    if df is None or analytics is None:
        st.info("Upload Excel to see analytics / Загрузите Excel для аналитики")
    else:
        st.subheader(t["summary"])
        show_metrics(t, analytics)
        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns(2)
        with left:
            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.subheader(t["verdicts"])
            st.dataframe(analytics["verdict_counts"], use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with right:
            st.markdown('<div class="soft-card">', unsafe_allow_html=True)
            st.subheader(t["ranges"])
            st.dataframe(analytics["score_ranges"], use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    if analytics is None:
        st.info("Upload Excel / Загрузите Excel")
    else:
        st.subheader(t["top10"])
        st.dataframe(filter_report_dataframe(analytics["top_10"], report_level), use_container_width=True)
        st.subheader(t["worst10"])
        st.dataframe(filter_report_dataframe(analytics["worst_10"], report_level), use_container_width=True)

with tabs[2]:
    if analytics is None:
        st.info("Upload Excel / Загрузите Excel")
    else:
        st.subheader(t["risk_stones"])
        st.dataframe(filter_report_dataframe(analytics["risk_df"], report_level), use_container_width=True)
        st.subheader(t["critical_risk"])
        st.dataframe(filter_report_dataframe(analytics["critical_df"], report_level), use_container_width=True)

with tabs[3]:
    if df is None:
        st.info("Upload Excel / Загрузите Excel")
    elif "Report #" in df.columns:
        st.subheader(t["stone_debug"])
        selected_report = st.selectbox(t["debug_select"], df["Report #"].astype(str).tolist())
        stone = df[df["Report #"].astype(str) == selected_report].iloc[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Kurgin Score", score_label(stone["Kurgin Score"]))
        col2.metric("Triple Score", score_label(stone["Triple Score"]))
        col3.metric("Structure Modifier", score_label(stone["Structure Modifier"]))
        st.markdown('<div class="soft-card">', unsafe_allow_html=True)
        st.write(f"### {t['verdict']}")
        st.write(stone["Verdict Local"])
        st.write(f"### {t['tags']}")
        st.write(stone["Tags Local"] if stone["Tags Local"] else "—")
        st.write(f"### {t['risks_title']}")
        st.write({"Visual Check": stone["Visual Check"], "Critical Risk": stone["Critical Risk"]})
        st.markdown('</div>', unsafe_allow_html=True)
        diagnostics_cols = ["Nailhead", "Fisheye", "Fire Loss", "Depth Dev", "Crown Dev", "Pavilion Dev", "Balance Err", "Girdle Penalty"]
        st.write(f"### {t['diagnostics']}")
        st.dataframe(stone[diagnostics_cols].to_frame(name="Value"), use_container_width=True)
        if report_level in ["Full Report", "Professional Report"]:
            st.write(f"### {t['breakdown']}")
            st.text(stone["Breakdown"])
        st.write(f"### {t['full_data']}")
        st.dataframe(filter_report_dataframe(pd.DataFrame([stone]), report_level).T, use_container_width=True)

with tabs[4]:
    st.subheader(t["certificate"])
    st.info(t["certificate_hint"])
    cam_img = st.camera_input("Сфотографировать сертификат / Take certificate photo")
    file_img = st.file_uploader("Загрузить фото сертификата / Upload certificate image", type=["jpg", "jpeg", "png"])
    img = cam_img or file_img
    if img:
        st.image(img, caption="Certificate preview / Предпросмотр сертификата", use_container_width=True)
    with st.form("certificate_manual_form"):
        report = st.text_input("Report #", value="")
        shape = st.selectbox("Shape", ["ROUND", "OVAL", "PEAR", "CUSHION", "EMERALD", "RADIANT", "PRINCESS"])
        c1, c2, c3 = st.columns(3)
        crown_angle = c1.number_input("Crown Angle", value=34.5)
        pavilion_angle = c2.number_input("Pavilion Angle", value=40.75)
        table_percent = c3.number_input("Table %", value=56.0)
        c4, c5, c6, c7 = st.columns(4)
        depth_percent = c4.number_input("Depth %", value=61.5)
        crown_percent = c5.number_input("Crown %", value=15.0)
        pavilion_percent = c6.number_input("Pavilion %", value=43.0)
        girdle_percent = c7.number_input("Girdle %", value=3.5)
        submitted = st.form_submit_button("Рассчитать камень / Calculate stone")
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
        stone = process_single_stone(params)
        st.write("### Result / Результат")
        st.dataframe(filter_report_dataframe(pd.DataFrame([stone]), report_level), use_container_width=True)
        if report_level in ["Full Report", "Professional Report"] and "Breakdown" in stone:
            st.text(stone["Breakdown"])

with tabs[5]:
    if df is None:
        st.info("Upload Excel / Загрузите Excel")
    else:
        st.subheader(t["raw_table"])
        st.dataframe(filter_report_dataframe(df, report_level), use_container_width=True)

with tabs[6]:
    if df is None or analytics is None:
        st.info("Upload Excel / Загрузите Excel")
    else:
        st.subheader(t["download_result"])
        excel_data = create_excel_output(df, analytics, mapping_df=mapping_df, report_level=report_level)
        st.download_button(label=t["download_excel"], data=excel_data, file_name="kurgin_score_result.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

with tabs[7]:
    st.subheader("Access Admin / Админка доступа")
    st.caption("MVP: настройки сохраняются в access_settings.json")
    new_settings = {}
    for r in ROLES:
        new_settings[r] = st.multiselect(f"{r}", REPORT_LEVELS, default=access_settings.get(r, []))
    if st.button("Save Access Settings / Сохранить настройки доступа"):
        save_access_settings(new_settings)
        st.success("Saved / Сохранено")
