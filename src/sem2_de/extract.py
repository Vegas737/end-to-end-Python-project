import argparse
import yaml
import requests
import os
import json

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_extract(config_path, run_date):
    config = load_config(config_path)
    
    base_url = config['api']['base_url']
    country = config['entity']['country_code']
    
    year = run_date.split('-')[0]
    url = f"{base_url}/{year}/{country}"
    
    print(f"--- Этап Extract: Запрос данных за {run_date} ---")
    print(f"Начинаю выгрузку данных из API: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        out_dir = "/opt/airflow/data/raw"
        os.makedirs(out_dir, exist_ok=True)
        
        file_path = os.path.join(out_dir, f"raw_{run_date}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Успех! Данные сохранены в: {file_path}")
        print(f"Получено записей: {len(data)}")

    except Exception as e:
        print(f"❌ Произошла ошибка при выгрузке: {e}")
        raise e 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--date", type=str, required=True) 
    args = parser.parse_args()
    
    run_extract(args.config, args.date)
