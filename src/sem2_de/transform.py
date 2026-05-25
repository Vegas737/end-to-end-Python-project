import argparse
import pandas as pd
import json
import os

def transform(run_date):
    print(f"--- Этап Transform: Очистка данных за {run_date} ---")
    
    input_file = f'/opt/airflow/data/raw/raw_{run_date}.json'
    
    if not os.path.exists(input_file):
        print(f"❌ Файл {input_file} не найден. Проверь этап Extract!")
        return False
        
    print(f"Обработка файла: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("⚠ Получен пустой массив данных от API")
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(data)
    
    if 'date' in df.columns and not df.empty:
        df['date'] = pd.to_datetime(df['date'])
    
    os.makedirs('/opt/airflow/data/normalized', exist_ok=True)
    
    out_path = f'/opt/airflow/data/normalized/normalized_{run_date}.csv'
    df.to_csv(out_path, index=False)
    
    print(f"✅ Данные нормализованы и сохранены в {out_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--date", type=str, required=True)  
    args = parser.parse_args()

    if transform(args.date):
        exit(0)
    else:
        exit(1)
