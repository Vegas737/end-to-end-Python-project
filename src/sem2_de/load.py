import pandas as pd
from sqlalchemy import create_engine
import os

conn_url = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(conn_url)

normalized_file = "data/normalized/holidays_cleaned.csv"

if os.path.exists(normalized_file):
    df = pd.read_csv(normalized_file)
    print(f"✅ Загружаем данные из слоя Normalized: {normalized_file}")
    
    with engine.begin() as connection:
        df.to_sql(
            name='mart_holidays_germany', 
            con=connection, 
            if_exists='replace',
            index=False
        )
    print(f"✅ Успешно загружено {len(df)} строк в таблицу 'mart_holidays_germany'")
else:
    print(f"❌ Ошибка: Файл {normalized_file} не найден. Проверь этап Transform!")
    exit(1)
