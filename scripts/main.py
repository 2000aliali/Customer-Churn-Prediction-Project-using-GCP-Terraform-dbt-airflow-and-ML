import psycopg2
import csv
import xml.etree.ElementTree as ET
from google.cloud import storage
from google.oauth2 import service_account
import pandas as pd 

# Specify your Cloud Storage bucket name and the XML file path
bucket_name = 'bucket_dbdata'  # Your GCS bucket name
destination_blob_name = 'bank_data.xml'  # Name in GCS

# Service account key file
key_path = 'C:\\Users\\Lenovo\\Desktop\\GCP-Project_2\\key.json'
credentials = service_account.Credentials.from_service_account_file(key_path)

# Local PostgreSQL connection details
local_db_config = {
    'dbname': 'dbdata',
    'user': 'postgres',
    'password': 'Aliel2000@',
    'host': 'localhost',
    'port': '5432'
}

csv_file_path = 'C:/Users/Lenovo/Desktop/GCP-Project_2/bank_datastored_in_postgresql.csv'
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

# Establish connections
try:
    local_conn = psycopg2.connect(**local_db_config)
    
except Exception as e:
    print(f"Error connecting to the databases: {e}")
    exit(1)

# Create cursors
local_cursor = local_conn.cursor()




# now we shoud first create a table in our database db_name that we creates from cloud sql
create_table_sql = """
CREATE TABLE IF NOT EXISTS churn_modelling 
(
    rownumber integer NOT NULL,
    customerid integer,
    surname character varying(50) COLLATE pg_catalog."default",
    creditscore integer,
    geography character varying(50) COLLATE pg_catalog."default",
    gender character varying(20) COLLATE pg_catalog."default",
    age integer,
    tenure integer,
    balance double precision,
    numofproducts integer,
    hascrcard integer,
    isactivemember integer,
    estimatedsalary double precision,
    exited integer,
    CONSTRAINT churn_modelling_pkey PRIMARY KEY (rownumber)
);
"""


# ****************** migrate the data of local postgresql *********************** #
# Path to the local CSV file
local_csv_path = 'local_data_export_from postgresql.csv' 


# Migrate data from local PostgreSQL
fetch_query = "SELECT rownumber, customerid, surname, creditscore, geography, gender, age, tenure, \
               balance, numofproducts, hascrcard, isactivemember, estimatedsalary, exited FROM churn_modelling;"  # Replace with your actual table name

try:
    local_cursor.execute(fetch_query)
    local_rows = local_cursor.fetchall()


        # Write data to CSV
    with open(local_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['rownumber', 'customerid', 'surname', 'creditscore', 'geography', 
                             'gender', 'age', 'tenure', 'balance', 'numofproducts', 
                             'hascrcard', 'isactivemember', 'estimatedsalary', 'exited'])  # Header
        csv_writer.writerows(local_rows)
    print("Local data exported to CSV successfully.")

    

except Exception as e:
    print(f"Error during local data migration: {e}")
upload_to_gcs('bucket_dbdata', csv_file_path, 'bank_data.csv')
print("Local data migration from postgresql to gloud storage completed successfully.")

#********************** Migrate data from XML*******************************# 
# Load the XML file
xml_file_path = 'C:/Users/Lenovo/Desktop/GCP-Project_2/bank_data.xml'
tree = ET.parse(xml_file_path)
root = tree.getroot()
# Initialize a list to store the data
data = []

# Extract data from XML
for customer in root.findall('./Customers/Customer'):
    customer_data = {
        'CustomerID': customer.get('id'),
        'RowNumber': customer.get('RowNumber'),
        'Surname': customer.find('./PersonalInfo/Surname').text,
        'Gender': customer.find('./PersonalInfo/Gender').text,
        'Age': customer.find('./PersonalInfo/Age').text,
        'Geography': customer.find('./PersonalInfo/Geography').text,
        'CreditScore': customer.find('./Financials/CreditScore').text,
        'Balance': customer.find('./Financials/Balance').text,
        'EstimatedSalary': customer.find('./Financials/EstimatedSalary').text,
        'Tenure': customer.find('./AccountDetails/Tenure').text,
        'NumOfProducts': customer.find('./AccountDetails/NumOfProducts').text,
        'HasCrCard': customer.find('./AccountDetails/HasCrCard').text,
        'IsActiveMember': customer.find('./AccountDetails/IsActiveMember').text,
        'Exited': customer.find('./Status/Exited').text,
    }
    data.append(customer_data)

# Create a DataFrame and save to CSV
df = pd.DataFrame(data)
csv_file_path = 'C:/Users/Lenovo/Desktop/GCP-Project_2/bank_datastored_in_xml.csv'
df.to_csv(csv_file_path, index=False)

# Upload CSV file to Google Cloud Storages


# Call the upload function
upload_to_gcs('bucket_dbdata', csv_file_path, 'bank_data.csv')
