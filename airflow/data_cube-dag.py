# TO DO
# update data_cube scripts and put them in operator folders, write README,

import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# import scripts
from airflow.operators.data_cube_1 import process_providers
from airflow.operators.data_cube_2 import process_population


def consumer_operator(consumer, **kwargs):
    output_path = kwargs['dag_run'].conf.get("output_path", None)
    if output_path:
        consumer(output_path)
    else:
        consumer()


def fetch_data(url, output_path):
    response = requests.get(url, stream=True, verify=False)

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=5000):
            f.write(chunk)
    return response


dag_args = {
    "email": ["alex.r.dore@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    'retry_delay': timedelta(minutes=15)
}

with DAG(
        dag_id="data-cubes",
        default_args=dag_args,
        start_date=datetime(2023, 3, 20),
        schedule=None,
        catchup=False,
        tags=["NDBI046"],
) as dag:
    # Care Providers

    task01 = PythonOperator(
        task_id="get-care-providers-dataset",
        python_callable=fetch_data,
        op_args=["https://opendata.mzcr.cz/data/nrpzs/narodni-registr-poskytovatelu-zdravotnich-sluzeb.csv"]
    )
    task01.doc_md = """\
    Downloads care provider dataset
    """

    task02 = PythonOperator(
        task_id="transform-care-providers",
        python_callable=consumer_operator,
        op_args=[process_providers]
    )
    task02.doc_md = """\
    Transforms the data from the csv file and generates a ttl file.
    """

    # Population 2021

    task03 = PythonOperator(
        task_id="get-population-2021-dataset",
        python_callable=fetch_data,
        op_args=["https://www.czso.cz/documents/10180/184344914/130141-22data2021.csv"]
    )
    task03.doc_md = """\
    Downloads population dataset.
    """

    task04 = PythonOperator(
        task_id="get-county-codelist-dataset",
        python_callable=fetch_data,
        op_args=[
            "https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02/číselník-okresů-vazba-101-nadřízený.csv",
            False
        ]
    )
    task04.doc_md = """\
    Downloads Codelist dataset.
    """

    task05 = PythonOperator(
        task_id="transform-population-2021",
        python_callable=consumer_operator,
        op_args=[process_population]
    )
    task05.doc_md = """\
     Transforms the data from the population CSV file and generates a ttl file.
     """

    task01 >> task02
    [task03, task04] >> task05


