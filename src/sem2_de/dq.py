import pandas as pd
import json
import os
import glob

def run_dq_checks():
    folder_path = 'data/normalized/variant_20/'
    files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not files:
        return [{"check": "file_exists", "status": "FAIL", "details": "No CSV files found"}]
    
    latest_file = max(files, key=os.path.getctime)
    df = pd.read_csv(latest_file)
    
    if 'holiday_date' in df.columns:
        df = df.rename(columns={'holiday_date': 'date'})
    df['date'] = pd.to_datetime(df['date'])

    report = []

    is_not_empty = len(df) > 0
    report.append({
        "check": "table_not_empty",
        "status": "PASS" if is_not_empty else "FAIL",
        "details": f"Rows: {len(df)}"
    })

    no_null_dates = df['date'].notna().all()
    report.append({
        "check": "no_null_dates",
        "status": "PASS" if no_null_dates else "FAIL",
        "details": "All dates must be present"
    })

    is_unique = not df.duplicated(subset=['date', 'eng_name']).any()
    report.append({
        "check": "unique_holidays",
        "status": "PASS" if is_unique else "FAIL",
        "details": "Business key (date + name) check"
    })

    only_2025 = (df['date'].dt.year == 2025).all()
    report.append({
        "check": "year_is_2025",
        "status": "PASS" if only_2025 else "WARNING",
        "details": "Data should only contain 2025 holidays"
    })

    all_public = (df['category'] == 'Public').all()
    report.append({
        "check": "only_public_holidays",
        "status": "PASS" if all_public else "WARNING",
        "details": "Unexpected holiday categories found"
    })

    os.makedirs('data', exist_ok=True)
    with open('data/dq_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
    print(f"✅ DQ Report generated for: {os.path.basename(latest_file)}")
    return report

if __name__ == "__main__":
    run_dq_checks()