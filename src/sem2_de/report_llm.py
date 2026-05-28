import os
import json
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def generate_llm_report():
    print("--- Этап Report: Генерация РЕАЛЬНОЙ LLM-сводки через YandexGPT (Алиса AI) ---")
    
    api_key = os.getenv("YANDEX_API_KEY")
    folder_id = os.getenv("YANDEX_FOLDER_ID")
    
    if not api_key or not folder_id:
        print("Ошибка: В .env не найдены YANDEX_API_KEY или YANDEX_FOLDER_ID!")
        return

    conn_url = "postgresql+psycopg2://student:student_pw@localhost:5433/analytics"
    engine = create_engine(conn_url)
    
    metrics_query = """
        SELECT 
            COUNT(*)::int as total_records,
            COUNT(DISTINCT "localName")::int as unique_holidays
        FROM mart_holidays_germany;
    """
    
    try:
        df_metrics = pd.read_sql(metrics_query, con=engine)
        total_rows = int(df_metrics['total_records'].iloc[0])
        unique_names = int(df_metrics['unique_holidays'].iloc[0])
        print(f"Из базы успешно считано строк: {total_rows}, уникальных праздников: {unique_names}")
    except Exception as e:
        print(f"Ошибка при чтении таблицы из базы: {e}")
        return
    
    final_prompt = (
        f"На основе предоставленного контекста напиши краткий бизнес-анализ.\n"
        f"Данные из базы:\n"
        f"- Анализируемый год: 2026\n"
        f"- Всего строк в базе: {total_rows}\n"
        f"- Уникальных наименований праздников: {unique_names}\n\n"
        f"Сгенерируй отчет в формате Markdown с обязательными разделами: '### Бизнес-интерпретация' и '### Рекомендации'."
    )

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "x-folder-id": folder_id,
        "Content-Type": "application/json"
    }
    
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "user",
                "text": final_prompt  
            }
        ]
    }



    print("Отправка запроса в YandexGPT API...")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result_json = response.json()
        llm_interpretation = result_json['result']['alternatives'][0]['message']['text']
    except Exception as e:
        print(f"Ошибка при запросе к YandexGPT API: {e}")
        if 'response' in locals() and response.text:
            print(f"Детали ответа Яндекса: {response.text}")
        return

    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    project_root = os.path.abspath(os.path.join(current_dir, "../..")) 
    target_dir = os.path.join(project_root, "docs", "llm")
    os.makedirs(target_dir, exist_ok=True)
    
    report_path = os.path.join(target_dir, "summary.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"## Финальный аналитический отчет (YandexGPT Summary)\n\n")
        f.write(f"**Дата генерации:** 2026-05-28\n\n")
        f.write(llm_interpretation)
        
    print(f"LLM-отчет успешно сгенерирован и сохранен в: {report_path}")
    log_path = os.path.join(project_root, "LLM_Usage_Log.md")
    
    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write("# Журнал использования YandexGPT API\n\n")
            log_file.write("| Дата запуска | Статус | Считано строк из БД | Модель |\n")
            log_file.write("| --- | --- | --- | --- |\n")
            
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"| 2026-05-28 | SUCCESS | {total_rows} строк / {unique_names} праздников | yandexgpt-lite |\n")
        
    print(f"Запись успешно добавлена в лог: {log_path}")

if __name__ == "__main__":
    generate_llm_report()