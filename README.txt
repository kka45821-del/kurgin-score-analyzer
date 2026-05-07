Kurgin Score Analyzer v1.4-architecture

Run:
python -m streamlit run app.py

v1.4 changes:
- App architecture foundation improved
- Added formula_modules/ for future formula development
- Added centralized platform_config/
- Added StoneInput object model
- Added validation layer
- Excel processing now uses validation before formula calculation
- Unsupported shapes and validation errors are handled more cleanly
- Formula core remains unchanged by design

Existing features:
- Excel upload
- Column Mapping
- Kurgin Score engine for ROUND
- Unsupported shapes marked IN DEVELOPMENT
- RU/EN UI
- Config System
- Report levels and access roles
- Certificate camera/upload MVP
- Manual certificate calculation
- Excel export with Column Mapping sheet
