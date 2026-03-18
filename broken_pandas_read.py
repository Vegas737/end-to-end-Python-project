import pandas as pd
from io import StringIO

csv_text = "id;value\n1;10\n2;20\n3;30\n"

df = pd.read_csv(StringIO(csv_text),sep=";")

print(df.dtypes)

try:
    print("Среднее значение value:", df["value"].mean())
except Exception as e:
    print(f"ОШИБКА: Не удалось посчитать среднее. Причина: {e}")

print("TECT 1/ Пустая строка.\n")
csv_text_2 = "id;value\n1;10\n\n3;30\n"
df2 = pd.read_csv(StringIO(csv_text_2), sep=";")
print(f"Количество строк в df2: {len(df2)}")
print(df2)

print("TECT 2/ Пропуск в value.\n")
csv_text_3 = "id;value\n1;10\n2;\n3;30\n"
df3 = pd.read_csv(StringIO(csv_text_3), sep=";")
print("Типы данных df3:")
print(df3.dtypes)
print("Среднее df3:", df3["value"].mean())
print(df3)