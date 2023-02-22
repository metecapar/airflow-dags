from datetime import datetime, timedelta
from airflow import DAG
from airflow.configuration import conf
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.bash import BashOperator



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='example_kubernetes_pod', 
    schedule='@once', 
    default_args=default_args
) as dag: KubernetesPodOperator(
        namespace='dev',
        image="hello-world",
        labels={"test": "mete"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=False,  # if set to true, will look in the cluster, if false, looks for file
        #config_file='/opt/airflow/configfile/config.json', 
        kubernetes_conn_id='matador',
        is_delete_operator_pod=True,
        get_logs=True
    )