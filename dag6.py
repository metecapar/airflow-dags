from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
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
        image='hello-world',
        kubernetes_conn_id='matador',
        is_delete_operator_pod=False,
        get_logs=True,
    )

    docker_task = DockerOperator(
        task_id='docker_task',
        image='hello-world',
        command='echo "Hello, Docker!"',
        api_version='auto',
        auto_remove=False,
    )

    kubernetes_task >> docker_task