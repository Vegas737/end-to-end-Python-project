import pandas as pd
from sqlalchemy import create_engine
import os

conn_url = "postgresql+psycopg2://student:student_pw@postgres:5432/analytics"
engine = create_engine(conn_url)

normalized_file = "/opt/airflow/data/normalized/holidays_cleaned.csv"

if os.path.exists(normalized_file):
    df = pd.read_csv(normalized_file)
    print(f"Загружаем данные из слоя Normalized: {normalized_file}")
    
    with engine.begin() as connection:
        df.to_sql(
            name='mart_holidays_germany', 
            con=connection, 
            if_exists='replace',
            index=False
        )
    print(f"Успешно загружено {len(df)} строк в таблицу 'mart_holidays_germany'")
else:
    print(f"Ошибка: Файл не найден по пути: {os.path.abspath(normalized_file)}")
    exit(1)
