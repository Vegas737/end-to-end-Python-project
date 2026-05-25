import argparse
import pandas as pd
from sqlalchemy import create_engine, text
import os

def run_load(run_date):
    print(f"--- Этап Load: Загрузка периода {run_date} в БД ---")
    
    normalized_file = f"/opt/airflow/data/normalized/normalized_{run_date}.csv"

    if not os.path.exists(normalized_file):
        print(f"❌ Ошибка: Файл не найден: {normalized_file}")
        exit(1)
        
    df = pd.read_csv(normalized_file)
    print(f"Загружаем данные из слоя Normalized: {normalized_file}")
    
    target_year = int(run_date.split('-')[0])
    
    df['load_period_year'] = target_year

    conn_url = "postgresql+psycopg2://student:student_pw@postgres:5432/analytics"
    engine = create_engine(conn_url)
    
    with engine.begin() as connection:
        table_exists_query = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'mart_holidays_germany'
            );
        """)
        table_exists = connection.execute(table_exists_query).scalar()
        
        if table_exists:
            delete_query = text("DELETE FROM mart_holidays_germany WHERE load_period_year = :year")
            connection.execute(delete_query, {"year": target_year})
            print(f"🗑 Очищены старые данные в БД за {target_year} год.")
        else:
            print("🆕 Таблицы ещё не существует. Она будет создана автоматически.")

        df.to_sql(
            name='mart_holidays_germany', 
            con=connection, 
            if_exists='append',
            index=False
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--date", type=str, required=True) 
    args = parser.parse_args()

    run_load(args.date)
