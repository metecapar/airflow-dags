from airflow.models import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
import urllib3
import requests,psycopg2

db = Variable.get("db")
dbPassword = Variable.get("pass")
user = Variable.get("user")
rabbitHost = Variable.get("rabbitHost")

hostname = rabbitHost
username = "user"
password = "password"

def getDefinition():
    headers = urllib3.make_headers(basic_auth=username + ":" + password)
    url = "http://"+hostname+":15672/api/definitions"
    response = requests.request("GET", url, headers=headers)
    definition = response.text
    writeData(definition)

def writeData(definition):
    conn = psycopg2.connect(host=db, database="devops_template", user=user, password=dbPassword, port="5432")
    imlec = conn.cursor()
    insertQuery = 'INSERT INTO defs (defsRabbitMQ) VALUES (%s);'
    value = (definition,)
    imlec.execute(insertQuery,value)
    conn.commit()
    



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}   
dag = DAG(
    dag_id='rabbitmq_definition_export_write_database',
    schedule='@daily', 
    default_args=default_args
) 
defSc = PythonOperator(
        task_id="definition_writer",
        python_callable=getDefinition,
        dag=dag
    )
defSc