from datetime import datetime, timedelta
from airflow import DAG
from airflow.configuration import conf
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.bash import BashOperator



matador = Variable.get('matador')
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
) as dag:
    bash_task_one = BashOperator(
        task_id="bash_task",
        bash_command='mkdir /opt/airflow/configfile'
    )
    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo "{{ var.value.matador }}" > /opt/airflow/configfile/config.json'
    )
    task_one = KubernetesPodOperator(
        namespace='dev',
        image="hello-world",
        labels={"test": "mete"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=False,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="",  # is ignored when in_cluster is set to True
        config_file='/opt/airflow/configfile/config.json', 
        is_delete_operator_pod=True,
        get_logs=True,
    )
    bash_task_one>>bash_task >> task_one