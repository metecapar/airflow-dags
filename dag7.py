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
    'kubernetes_queue_check',
    default_args=default_args,
    concurrency=1,
    schedule_interval='*/5 * * * *'
)
with dag:
    kubernetes_task = KubernetesPodOperator(
        task_id='kubernetes_task',
        name='kubernetes-fo-task',
        namespace='dev',
        image="platform360.azurecr.io/ford-queue-checker:1.0.0",
        image_pull_secrets=[k8s.V1LocalObjectReference("acr")],
        kubernetes_conn_id='fo',
        is_delete_operator_pod=False,
        get_logs=True,
    )
    kubernetes_task