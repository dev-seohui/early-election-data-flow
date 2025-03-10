from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.extract.news_extract import NaverBlogExtractor
from scripts.load.news_load import PostgresLoader

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "naver_blog_to_postgres",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    catchup=False,
)

extractor = NaverBlogExtractor()
loader = PostgresLoader()

fetch_task = PythonOperator(
    task_id="fetch_naver_blog_data",
    python_callable=extractor.fetch_blog_data,
    dag=dag,
)

insert_task = PythonOperator(
    task_id="insert_into_postgres",
    python_callable=lambda: loader.insert_data(extractor.fetch_blog_data()),
    dag=dag,
)

fetch_task >> insert_task
