from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import requests
import json
import time

# NOTICE: in platform lessons and also in 3rd exercise it was specified to pull stock data daily and use dag daily also, but since on alphavantage site daily option is premium
# it won't work, so I made it so it runs weekly which is free to get on their site.

# define python logic
def get_data(**kwargs): # by writing '**kwargs' your airflow task is expecting a dictionary of arguments
    ticker = kwargs['ticker']
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    api_key = 'PK386GFVV4YIC5TI'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + ticker + '&apikey=' + api_key
    r = requests.get(url)
    try:
        data = r.json()
        path = 'C:\\Users\\sekil\\airflow\\data\\DATA_CENTAR\\DATA_LAKE\\'
        with open(path + 'stock_market_raw_data_' + ticker + '_' + str(time.time()), 'w') as outfile:
            json.dump(data, outfile)
    except:
        pass

# define default arguments
default_dag_args = {
    'start_date': datetime(2022, 9, 1),
    'email_on_failure': None,
    'email_on_retry': None,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'project_id': 1
}

#define DAG
with DAG('market_data_alphavantage_DAG', schedule_interval='@weekly', catchup=False, default_args=default_dag_args) as dag_python:
    # define tasks
    task_0 = PythonOperator(task_id = 'get_market_data', python_callable=get_data, op_kwargs={'ticker': 'IBM'})



