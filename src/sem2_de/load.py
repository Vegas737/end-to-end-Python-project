import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime

conn_url = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(conn_url)

mart_dir = "data/mart/variant_20"

files = [f for f in os.listdir(mart_dir) if f.startswith("mart_monthly")]
files.sort()
latest_mart = os.path.join(mart_dir, files[-1])

df = pd.read_csv(latest_mart)

with engine.begin() as connection:
    df.to_sql(
        name='mart_holidays_germany', 
        con=connection, 
        if_exists='replace', 
        index=False
    )

print(f"✅ Успешно загружено {len(df)} строк в таблицу 'mart_holidays_germany'")
print(f"Использован файл: {latest_mart}")
