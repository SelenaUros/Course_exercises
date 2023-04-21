from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

#define functions
def current_datetime():
    current_dateTime = datetime.now()
    print(current_dateTime)


# define default args
default_dag_args = {
    'start_date': datetime(2022, 9, 1),
    'email_on_failure': None,
    'email_on_retry': None,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'project_id': 1
}

# define DAG
with DAG('exercise_2', schedule_interval='@daily', catchup=False, default_args=default_dag_args) as dag_python:
    # define dag tasks
    task_0 = PythonOperator(task_id = 'current_datetime', python_callable=current_datetime)
