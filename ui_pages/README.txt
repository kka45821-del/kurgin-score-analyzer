Kurgin Score Analyzer v1.5 — Mobile-first PWA-ready interface

Main changes:
1. Two-mode product structure:
   - Diamond Analysis / Анализ бриллианта
   - Professional Analytics / Профессиональная аналитика
2. Report action buttons:
   - Score Only
   - Short Report
   - Detailed Analysis
   - Full Report
   - Professional Review
   - PDF / Certificate placeholder
3. Access gates:
   - Buttons remain visible.
   - Restricted levels show access messages instead of hiding the value.
4. Mobile-first UI:
   - app-like layout
   - bottom navigation
   - large action buttons
   - card-based results
5. Secure Formula Ready architecture:
   - formula_client/local_client.py
   - formula_client/cloud_client.py
   - formula_client/engine_client.py
   - FORMULA_MODE=local/cloud/cloud_fallback
   - FORMULA_API_URL and FORMULA_API_KEY ready for future Yandex Cloud Function

Current formula status:
- Formula still runs locally by default for stability.
- The site is now prepared to move calculation to a closed cloud API.

Run locally:
py -m streamlit run app.py

Deploy:
Push to GitHub. Streamlit Cloud auto-deploys from main/app.py.


v1.6 Score Analyzer Focus:
- Admin panel intentionally excluded from this branch.
- Improved app-like navigation.
- Added Reports screen for saved single/batch results.
- Added profile registration type selector.
- Added tag interpretation display for report levels.
- Continued cloud formula ready architecture.


v1.7 Interpretation Templates:
- Added template-based text generation for single stone and Excel output.
- Added short/detail interpretation, recommendation, warning and disclaimer columns.
- Added tag slots tag1-tag6 and tags_all.
- No commercial formula coefficients are exposed in generated text.


v1.8 Text Generator:
- Added score-band based text generation.
- Added polished text for 0-75 / 76-79 / 80-84 / 85-89 / 90-94 / 95-98 / 99-100.
- Replaced vague visual-check wording with a safer phrase:
  "если визуальный осмотр, фото или видео не выявляют нежелательных эффектов".
- Added executive_summary, score_band, score_band_label.
- Improved recommendations and warnings without exposing formula coefficients.


v1.9 Single Stone PDF Report:
- Added branded KURGIN Diamond Analysis Report PDF generator.
- PDF includes summary, certificate data, geometry, KURGIN analysis, risks, interpretation, recommendation and disclaimer.
- PDF does not expose formula coefficients or commercial scoring rules.
- Single stone "PDF / сертификат" action now creates a downloadable analytical report.


v1.9.1 Open Access:
- Temporarily removed role/access gating from the UI.
- All report levels, including PDF, are available for formula/report testing.
- Real roles and monetization should be implemented later in Admin/Auth layer.
