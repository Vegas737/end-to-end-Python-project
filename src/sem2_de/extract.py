import argparse
import yaml
import requests
import os
import json
from datetime import datetime

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_extract(config_path):
    config = load_config(config_path)
    
    base_url = config['api']['base_url']
    country = config['entity']['country_code']
    year = config['entity']['year']
    url = f"{base_url}/{year}/{country}"
    
    print(f"Начинаю выгрузку данных из API: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        out_dir = os.path.join("data", "raw")
        os.makedirs(out_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        file_path = os.path.join(out_dir, f"holidays_{country}_{year}_{timestamp}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Успех! Данные сохранены в: {file_path}")
        print(f"Получено записей: {len(data)}")

    except Exception as e:
        print(f"Произошла ошибка при выгрузке: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()
    

    run_extract(args.config)
