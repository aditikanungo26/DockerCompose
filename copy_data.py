from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'dag_id': 'copy_table_data',
    'start_date':datetime(2021, 5, 20),
    }
# [END default_args]

# [START instantiate_dag]
with DAG(**default_args) as dag:
          src = PostgresHook(postgres_conn_id='postgres_src')
          tgt = PostgresHook(postgres_conn_id='postgres_tgt')
          src_conn = src.get_conn()
          cursor = src_conn.cursor()
          cursor.execute("SELECT * FROM roles")
          tgt.insert_rows(table="roles", rows=cursor)
          print(cursor)
          
          