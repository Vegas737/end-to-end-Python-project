import pandas as pd
from sqlalchemy import create_engine
import os

conn_url = "postgresql+psycopg2://student:student_pw@localhost:5433/analytics"
engine = create_engine(conn_url)

normalized_file = "data/normalized/variant_20/2026-03-19_11-39-15_holidays_germany.csv"
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
    import os
    print(f"Ошибка: Файл не найден по пути: {os.path.abspath(normalized_file)}")
    exit(1)

