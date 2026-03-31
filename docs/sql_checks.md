# SQL Проверки (Неделя 5)

### 1. Проверка загрузки данных (валидация количества)
**Запрос:**
```sql
SELECT count(*) FROM mart_holidays_germany;

SELECT count(*) AS total_rows 
FROM mart_holidays_germany;
1. Количество строк в базе: 10

SELECT * FROM mart_holidays_germany 
LIMIT 5;
2. Образец данных (первые 3 строки):
таблица содержит все нужные колонки.

SELECT month, count(*) 
FROM mart_holidays_germany 
GROUP BY month 
HAVING count(*) > 1;
3. Дубликаты месяцев: Не обнаружены (ОК)

SELECT month, public_holidays, school_holidays 
FROM mart_holidays_germany 
ORDER BY public_holidays DESC 
LIMIT 1;
4. Месяц с пиком праздников: 2025-04-01 (3 дня)

SELECT count(*) AS null_values 
FROM mart_holidays_germany 
WHERE month IS NULL OR public_holidays IS NULL;
5. Количество пустых значений (NULL): 0

