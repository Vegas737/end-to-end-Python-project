import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="etl_pipeline_variant_20",
    start_date=pendulum.datetime(2026, 5, 1, tz="UTC"), 
    schedule="*/5 * * * *", 
    catchup=False,
) as dag:

    extract_task = BashOperator(
        task_id="extract_data",
        bash_command="python /opt/airflow/src/sem2_de/extract.py --config /opt/airflow/configs/variant_20.yml --date '{{ ds }}'",
    )

    transform_task = BashOperator(
        task_id="transform_data",
        bash_command="python /opt/airflow/src/sem2_de/transform.py --config /opt/airflow/configs/variant_20.yml --date '{{ ds }}'",
    )

    dq_task = BashOperator(
        task_id="data_quality_check",
        bash_command="python /opt/airflow/src/sem2_de/dq.py --config /opt/airflow/configs/variant_20.yml --date '{{ ds }}'",
    )

    load_task = BashOperator(
        task_id="load_to_postgres",
        bash_command="python /opt/airflow/src/sem2_de/load.py --config /opt/airflow/configs/variant_20.yml --date '{{ ds }}'",
    )

    extract_task >> transform_task >> dq_task >> load_task
