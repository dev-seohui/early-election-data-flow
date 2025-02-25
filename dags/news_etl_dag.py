# 
from airflow import DAG
from airflow.operator.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# 개별 모듈 불러오기
from scripts.fetch_news import fetch_news
from scripts.transform import transform_data
from scripts.load_to_db import load_to_db

# DAG 기본 설정


# DAG 정의

