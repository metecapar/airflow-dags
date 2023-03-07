from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from kubernetes.client import models as k8s
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'kubernetes_docker_example',
    default_args=default_args,
    schedule='@once'
)
with dag:
    kubernetes_task = KubernetesPodOperator(
        task_id='kubernetes_task',
        name='kubernetes-task',
        namespace='default',
        image="platform360.azurecr.io/pythonscripts:elasticchecker",
        image_pull_secrets=[k8s.V1LocalObjectReference("acr-airflow")],
        kubernetes_conn_id='matador',
        is_delete_operator_pod=False,
        get_logs=True,
    )
    kubernetes_task