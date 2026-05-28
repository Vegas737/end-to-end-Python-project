## Как запустить проект
1. Поднимите контейнеры: `docker-compose up -d`
2. Запустите пайплайн в Airflow (`localhost:8080`), чтобы наполнить базу.
3. Сгенерируйте отчет ИИ: `python src/sem2_de/report_llm.py`
