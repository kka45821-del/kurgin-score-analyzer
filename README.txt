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


v1.9.2 Expanded Fields + Measurements Parser:
- Expanded column mapping for supplier Excel files and IGI-style fields.
- Added manual input fields for certificate, visual, inclusion and geometry data.
- Added Measurements parser:
  MinDiameter, MaxDiameter, AvgDiameter, DepthMM, DiameterDiff, RoundnessDeviation.
- Added Cert comment parser:
  Growth Method, Diamond Type, Treatment notes.
- Expanded PDF report fields while keeping empty fields visible as "—" for now.


v1.9.3 Logo PDF:
- Added KURGIN logo asset to assets/kurgin_logo.jpg.
- Added logo to the first page of KURGIN Diamond Analysis Report PDF.
- PDF layout still avoids formula coefficients and commercial rule disclosure.


v1.9.4 Excel Output Standard:
- Excel export now creates a full workbook structure:
  Summary, Score Report, Full Analysis, Tags Texts, Risks, Top Stones,
  Worst Stones, Unsupported Shapes, Errors Validation, Verdicts, Score Ranges,
  Formula Version, Column Mapping, Requested Report.
- tag1-tag6 are always created and included in Score Report / Full Analysis / Tags Texts.
- Added score-band and interpretation columns to Excel output.
- Added formatting, filters, frozen headers and score color scale.


v1.9.5 Excel PDF Standard:
- Added PDF report metadata columns:
  KURGIN Report ID, PDF Report Status, PDF Report File, PDF Report URL, Report Template Version.
- Added PDF Reports sheet.
- Added full analysis package export:
  kurgin_score_result.xlsx + reports/{Report}_KURGIN_Report.pdf.
- Excel package links point to relative PDF paths inside reports/.
- PDF reports use the same single-stone PDF generator as one-stone analysis.


v1.9.6 Platform Import Standard:
- Added Import Ready sheet for KURGIN Platform upload.
- Added Data Dictionary sheet.
- Added KURGIN Import ID, Formula Output Version, Data Completeness %, Report Quality Status and PDF Generation Mode.
- Added tag categories: tag_light, tag_structure, tag_spread, tag_risk, tag_certificate, tag_commercial.
- Added future module placeholders: spread_score, spread_status, diameter_symmetry_score, diameter_symmetry_status, roundness_status, commercial_view, value_score.
- Excel + PDF package still generates one PDF per OK stone using the same single-stone report template.


v1.9.7 Unified Report Style:
- Added unified report schema shared by Excel, PDF, one-stone view and future KURGIN Platform card.
- Added Unified Report sheet and KURGIN Card sheet.
- Added Schema Sections sheet for stable section order.
- PDF now shows Data Completeness %, Report Quality Status, Formula Output Version and Report Template Version.
- Data Dictionary now comes from the unified schema.


v1.9.8 Supplier Upload Recognition:
- Improved recognition for Wilson, SUJAN and Hearts&Arrows supplier files.
- Added aliases for Stock#, CutGrade, FLORO, $/CT, CertificateFilename, Certificate#, FluorescenceIntensity, Depth%, Table%, CrownHeight, PavilionDepth, LaserInscription, Certcomment, GrowthType, Countryofpolishing and more.
- Added Length/Width/Height enrichment when Measurements is absent or incomplete.
- Added recognition of Hearts & Arrows, price per carat, total price and certificate metadata.
- Formula itself is unchanged.


v1.9.9 Compact Report Style:
- Compact Excel output: Results, Details, Issues, Column Mapping, Summary.
- Results is the first sheet and contains the essential list, tags, interpretation, dimensions and PDF-forming fields.
- Compact PDF is now 2 pages and uses the same essential fields as Results.
- Measurements parser remains active for Measurements and separate Length / Width / Height columns.
- PDF package still creates one PDF per OK stone through the same single-stone PDF template.


v1.10 Compact Output Refined:
- Reduced Excel output to exactly 3 sheets: Results, Details, System.
- Results is the main working sheet: scores, tags, dimensions, interpretation, recommendation, PDF status.
- System combines summary, issues, column mapping and compact data dictionary.
- Improved dimension recognition from MinDiameter / MaxDiameter / DepthMM in addition to Measurements and Length / Width / Height.
- PDF remains compact 2 pages and uses the same single-stone report template for one stone and batch exports.


v1.10.1 Compact Results + Issues:
- Results sheet now contains only calculated OK stones.
- Details sheet now contains only calculated OK stones.
- Added Issues sheet for unsupported shapes, validation errors, measurement parsing problems and limited-data warnings.
- Added Measurement Parse Status / Source / Warning.
- Added platform_import_status and recommended_pdf_priority.
- Added export modes:
  Excel only,
  Excel + PDF for TOP stones,
  Excel + PDF for all calculated stones.


v1.10.2 Fixed Score Bands:
- Official KURGIN Score bands fixed:
  98.5-100 Elite / Элитный
  95-98.49 Premium / Премиальный
  90-94.99 High / Высокое качество
  80-89.99 Standard / Стандартный
  70-79.99 Fair / Среднее качество
  50-69.99 Poor / Низкое качество
  0-49.99 Rejected / Не рекомендуется
- Updated text generator, recommendations and public labels to match the fixed scale.
- No mathematical formula changes.


v1.10.3 Measurement & Spread Research Module:
- Added ExpectedDiameter using 6.45 × carat^(1/3).
- Added SpreadDelta %, VisualSpreadStatus, DiameterSymmetryStatus, MeasurementConsistencyStatus.
- Added DiameterSpreadModifierPreview, ScoreClassCapPreview, AdjustedKURGINScorePreview and AdjustedScoreBandPreview.
- Official KURGIN Score is NOT changed.
- Module is display/research-only to test how diameter/spread should influence future formula versions.


v1.10.4 Upload Recognition & Data Quality:
- Added column mapping confidence and notes.
- Added upload quality fields:
  Upload Quality Status, Geometry Status, Missing Geometry Fields, Possible Scale Issues, Column Recognition Status.
- Added measurement conflict detection and Chosen Measurement Source.
- Missing required geometry no longer blocks the whole file; rows go to Issues.
- Added CATALOG_DATA_ONLY, MISSING_GEOMETRY and POSSIBLE_SCALE_ISSUE statuses.
- Upload UI now shows a short recognition summary after file upload.
- Main formula and official score logic remain unchanged.


v1.10.5 Diameter Policy Review:
- Added diameter policy layer:
  Diameter Policy Status, Action, Reason, High Score Diameter Flag.
- Flags high KURGIN Score stones where spread/roundness/measurement data may challenge Elite/Premium/High public class.
- Adds HIGH_SCORE_DIAMETER_REVIEW issue type.
- Official KURGIN Score remains unchanged.
- This is still a research/policy layer for deciding how diameter should influence public class later.


v1.10.6 PDF Identity + Localization:
- PDF now uses Russian/English bilingual labels by default.
- Stone title, report number, lab and stock number are shown in a prominent identity card on page 1.
- Report # is no longer hidden in a small subtitle.
- PDF remains compact and uses the same template for one-stone and batch PDF generation.
- Official KURGIN Score and formula are unchanged.


v1.10.7 Multilingual PDF Polish:
- PDF report now uses 4 languages in this order: Russian, English, Chinese, Armenian.
- Russian remains the primary language.
- Stone title and report number are prominently shown on page 1.
- Certificate/geometric labels and core report sections are multilingual.
- Batch PDF and one-stone PDF use the same multilingual template.
- Official KURGIN Score and formula are unchanged.
