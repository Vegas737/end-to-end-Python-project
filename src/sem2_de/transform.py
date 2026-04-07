import pandas as pd
import json
import os
import glob

def transform():
    print("--- Этап Transform: Очистка данных ---")
    
    list_of_files = glob.glob('data/raw/*.json')
    if not list_of_files:
        print("❌ Нет данных для трансформации")
        return False
    
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Обработка файла: {latest_file}")

    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    os.makedirs('data/normalized', exist_ok=True)
    out_path = 'data/normalized/holidays_cleaned.csv'
    df.to_csv(out_path, index=False)
    
    print(f"✅ Данные нормализованы и сохранены в {out_path}")
    return True

if __name__ == "__main__":
    if transform():
        exit(0)
    else:
        exit(1)