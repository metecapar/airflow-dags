from datetime import datetime, timedelta
from airflow import DAG
from airflow.configuration import conf
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator


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

namespace = conf.get('kubernetes', 'NAMESPACE')
# This will detect the default namespace locally and read the
# environment namespace when deployed to Astronomer.
if namespace =='default':
    config_file = matador
    in_cluster = False
else:
    in_cluster = True
    config_file = None

with DAG(
    dag_id='example_kubernetes_pod', 
    schedule='@once', 
    default_args=default_args
) as dag:
    KubernetesPodOperator(
        namespace=namespace,
        image="hello-world",
        labels={"<pod-label>": "<label-name>"},
        name="airflow-test-pod",
        task_id="task-one",
        in_cluster=in_cluster,  # if set to true, will look in the cluster, if false, looks for file
        cluster_context="docker-desktop",  # is ignored when in_cluster is set to True
        config_file=config_file,
        is_delete_operator_pod=True,
        get_logs=True,
    )