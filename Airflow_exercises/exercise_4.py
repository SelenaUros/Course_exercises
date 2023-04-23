from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner':'airflow',
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

#creating sql logic
create_query = '''
CREATE TABLE public.employee_table (id INT NOT NULL, name VARCHAR(50), age INT)
'''
insert_data_query = '''
INSERT INTO public.employee_table (id, name, age)
values(1, Uros, 27), (2, Selena, 40), (3, Jimmy, 20)
'''
calculating_average_query = '''
CREATE TABLE employee_average_age as
SELECT avg(age) as 'Employee average age' FROM employee_table
'''

# creating DAG
with DAG('postgres_dag_connection', default_args=default_args, schedule_interval=None, start_date=days_ago(1)):
    task_0 = PostgresOperator('creation_of_table', sql = create_query, postgres_conn_id = 'postgres_local')
    task_1 = PostgresOperator('insertion_of_data', sql = insert_data_query, postgres_conn_id = 'postgres_local')
    task_2 = PostgresOperator('calculating_average_age', sql = calculating_average_query, postgres_conn_id = 'postgres_local')

task_0 >> task_1 >> task_2







