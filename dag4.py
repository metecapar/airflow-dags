from airflow.models import DAG
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from python.rabbitmq.definitionExport import exportDef

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}   
with DAG(
    dag_id='rabbitmq_definition_export_write_database',
    schedule='@daily', 
    default_args=default_args
) as dag: PythonOperator(
        namespace='dev',
        task_id="definition_writer",
        kubernetes_conn_id='staging',
        is_delete_operator_pod=False,
        get_logs=True,
        python_callable=exportDef,
        dag=dag
    )