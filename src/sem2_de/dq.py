import argparse
import pandas as pd
import json
import os

def run_dq_checks(run_date):
    print(f"--- Этап Data Quality: Проверка периода {run_date} ---")
    
    input_file = f'/opt/airflow/data/normalized/normalized_{run_date}.csv'
    
    if not os.path.exists(input_file):
        print(f"❌ Файл {input_file} не найден!")
        return False
    
    df = pd.read_csv(input_file)
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    report = []
    has_fail = False

    is_not_empty = len(df) > 0
    status_empty = "PASS" if is_not_empty else "FAIL"
    if not is_not_empty: has_fail = True
    report.append({
        "check": "table_not_empty",
        "status": status_empty,
        "details": f"Rows count: {len(df)}"
    })

    if not df.empty:
        no_null_dates = df['date'].notna().all()
        status_dates = "PASS" if no_null_dates else "FAIL"
        if not no_null_dates: has_fail = True
        report.append({
            "check": "no_null_dates",
            "status": status_dates,
            "details": "All dates must be present"
        })

        name_col = 'eng_name' if 'eng_name' in df.columns else (df.columns[1] if len(df.columns) > 1 else df.columns[0])
        is_unique = not df.duplicated(subset=['date', name_col]).any()
        status_unique = "PASS" if is_unique else "FAIL"
        if not is_unique: has_fail = True
        report.append({
            "check": "unique_holidays",
            "status": status_unique,
            "details": f"Business key check on columns: date + {name_col}"
        })

        target_year = int(run_date.split('-')[0])
        correct_year = (df['date'].dt.year == target_year).all()
        report.append({
            "check": f"year_is_{target_year}",
            "status": "PASS" if correct_year else "WARNING",
            "details": f"Data contains unexpected years for run period {target_year}"
        })

    os.makedirs('/opt/airflow/data/reports', exist_ok=True)
    report_path = f'/opt/airflow/data/reports/dq_report_{run_date}.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
    print(f"📋 DQ Report сохранен в: {report_path}")
    
    for check in report:
        print(f"[{check['status']}] {check['check']}: {check['details']}")
        
    if has_fail:
        print("❌ Критическая ошибка контроля качества! Остановка пайплайна.")
        return False
        
    print("✅ Все критические проверки качества пройдены успешно!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--date", type=str, required=True)
    args = parser.parse_args()

    if run_dq_checks(args.date):
        exit(0)
    else:
        exit(1) 
