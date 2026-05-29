import pandas as pd

from kurgin_core import analyze_dataframe, analyze_stone, export_excel, export_pdf, get_version_info


def test_one_stone():
    result = analyze_stone({
        "Shape": "ROUND",
        "Report #": "TEST123",
        "Lab": "IGI",
        "Weight": 1.00,
        "Color": "F",
        "Clarity": "VS1",
        "Measurements": "6.430x6.470x3.970",
        "CrownAngle": 34.5,
        "PavilionAngle": 40.8,
        "TablePercent": 56,
        "DepthPercent": 61.5,
        "CrownPercent": 15,
        "PavilionPercent": 43,
        "GirdlePercent": 3.5,
    })
    assert result["Calculation Status"] == "OK"
    assert result["Kurgin Score"] is not None
    assert "interpretation_short_ru" in result
    assert len(export_pdf(result)) > 1000


def test_batch_excel():
    df = pd.DataFrame([{
        "Report Number": "TEST123",
        "Cut Shape": "ROUND",
        "Weight": 1.00,
        "Color": "F",
        "Clarity": "VS1",
        "Measurements": "6.430x6.470x3.970",
        "Crown Angle": 34.5,
        "Pavilion Angle": 40.8,
        "Table %": 56,
        "Depth%": 61.5,
        "Crown Height": 15,
        "Pavilion Depth": 43,
        "Girdle %": 3.5,
    }])
    batch = analyze_dataframe(df)
    assert batch.dataframe.loc[0, "Calculation Status"] == "OK"
    assert len(export_excel(batch)) > 1000


if __name__ == "__main__":
    test_one_stone()
    test_batch_excel()
    print(get_version_info())
    print("OK")
