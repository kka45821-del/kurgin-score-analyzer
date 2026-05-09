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
