from visual_market_validation.analyze_validation_results import export_analysis_outputs

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Analyze filled visual/market validation workbook.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    print(json.dumps(export_analysis_outputs(args.input, args.output_dir), ensure_ascii=False, indent=2))
