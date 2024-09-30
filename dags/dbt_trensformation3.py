from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from google.cloud import bigquery
from datetime import datetime

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 29),
    'retries': 1,
}

# Initialize BigQuery client
client = bigquery.Client()


# Define the DAG
with DAG('dbt_transformations2',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    # Task to load CSV files into BigQuery
    load_csv_to_bq = GCSToBigQueryOperator(
        task_id='load_csv_to_bq',
        bucket='bucket_dbdata',
        source_objects=['bank_data_postgresql.csv'],
        destination_project_dataset_table='seconde-gcp-project.dataset_bank.raw_data_from_postgresql_and_xml_files',
        source_format='CSV',
        write_disposition='WRITE_APPEND',
        autodetect=False,  # Set to False since you're providing a schema
        schema_fields=[
            {'name': 'rownumber', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'customerid', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'surname', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'creditscore', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'geography', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'gender', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'age', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'tenure', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'balance', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'numofproducts', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'hascrcard', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'isactivemember', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'estimatedsalary', 'type': 'FLOAT', 'mode': 'NULLABLE'},
            {'name': 'exited', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        ],
        skip_leading_rows=1,
    )

    # Task to clean dbt environment
    dbt_clean = BashOperator(
        task_id='dbt_clean',
        bash_command='cd /home/airflow/gcs/data/gcp_project && dbt clean --profiles-dir .'
    )

    # Task to debug dbt configuration
    dbt_debug = BashOperator(
        task_id='dbt_debug',
        bash_command='cd /home/airflow/gcs/data/gcp_project && dbt debug --profiles-dir .'
    )

    # Task to run dbt transformations
    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='cd /home/airflow/gcs/data/gcp_project && dbt run --profiles-dir .'
    )

    # Task dependencies
    load_csv_to_bq >> dbt_clean >> dbt_debug >> run_dbt
