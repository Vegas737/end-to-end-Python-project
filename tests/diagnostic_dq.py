import pandas as pd

df = pd.DataFrame({"x": [1, None, 3]})

print("--- Тестируем ошибку ---")
try:
    assert df["x"].notna, "x has nulls"
    print("Тест прошел (это плохо!), хотя в данных есть NULL. Ошибка не поймана.")
except AssertionError:
    print("Тест упал. Ошибка поймана.")

print("\n--- Тестируем исправление ---")
try:
    assert df["x"].notna().all(), "x has nulls"
    print("Тест прошел.")
except AssertionError:
    print("Тест упал! Теперь мы реально видим, что в данных есть NULL.")