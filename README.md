# Customer-Churn-Prediction-Project-using-GCP-Terraform-dbt-and-ML


## Project Overview
The **Customer Churn Prediction Project** is designed to analyze customer data and predict the likelihood of customer churn using Google Cloud Platform (GCP) tools, Terraform for infrastructure management, dbt for data transformation, and machine learning techniques. The project involves extracting data from XML files, loading it into Google Cloud Storage (GCS), transferring it to BigQuery, transforming the data with dbt, and ultimately building a predictive model using Random Forest. The results are visualized through a dashboard created using Looker, and a user interface is built using Streamlit for model deployment.


## System Architecture
![Screenshot](https://github.com/2000aliali/Customer-Churn-Prediction-Project-using-GCP-Terraform-dbt-airflow-and-ML/blob/main/IMAGES/aaarch.jpg)

### To see our results, feel free to visit these two links:  
- [Looker Studio Dashboard](https://lookerstudio.google.com/u/0/reporting/8342ae48-032f-4100-b749-79e3c95c548f/page/tEnnC?s=r3vkVXjrVSo)  
- [Customer Churn Prediction Streamlit App](https://customer-churn-ali-el-azzaouy.streamlit.app/)

## Tools and Technologies Used
- **Google Cloud Platform (GCP)**: For cloud storage, data warehousing, and orchestration.
- **Terraform**: For infrastructure as code, automating the creation of GCP resources such as storage buckets and BigQuery datasets.
- **Apache Airflow (Cloud Composer)**: For orchestrating the data pipeline tasks and managing workflows.
- **BigQuery**: As the data warehouse to store and analyze large datasets.
- **dbt (data build tool)**: For data transformation and modeling.
- **Random Forest**: For building the machine learning model to predict customer churn.
- **Looker**: For creating a dashboard to visualize data insights.
- **Streamlit**: For developing a user-friendly web application to interact with the predictive model.

## Step-by-Step Implementation

### Step 1: Data Extraction
- **Source**: Data is extracted from XML files and a local CSV file containing customer information.
- **Local Environment**: Initial data processing is done on a local machine to prepare the data for loading into GCP.

### Step 2: Data Loading to GCP
- **Google Cloud Storage (GCS)**: The cleaned data is loaded into GCS under the bucket named `bucket_dbdata`.
- **Data Transfer to BigQuery**: The `GCSToBigQueryOperator` is used to transfer data from GCS to a BigQuery dataset named `dataset_bank`. This operator automates the ingestion of data from GCS into BigQuery tables.

### Step 3: Data Transformation using dbt
- **Transformation**: dbt is employed to transform the data in BigQuery. The transformations create three views:
  - **age_correlation**: To analyze the relationship between age and churn.
  - **aggregated_data**: To aggregate various metrics related to customer churn.
  - **salary_correlation**: To explore the relationship between salary and churn.
- **Workflow**: dbt tasks are orchestrated using Airflow, ensuring a clean and efficient transformation process.

### Step 4: Model Development
- **Data Preparation**: The raw dataset from BigQuery is loaded into a Pandas DataFrame, where irrelevant columns are dropped, and categorical features are encoded.
- **Random Forest Model**: A Random Forest classifier is trained on the cleaned dataset to predict customer churn. The model's performance is evaluated using metrics such as confusion matrix and classification report.

### Step 5: Model Serialization
- **Model Saving**: The trained Random Forest model is serialized using `joblib` to save it as a `.pkl` file for future use and deployment.

### Step 6: Dashboard Creation
- **Looker Dashboard**: A dashboard is created using Looker to visualize insights from the data, including trends related to customer churn and key performance indicators.

### Step 7: User Interface Development
- **Streamlit Application**: A web application is developed using Streamlit to provide an interface for users to input customer data and receive churn predictions from the trained model. This interface is deployed on Streamlit Cloud, making it accessible for users.

## Infrastructure Setup with Terraform
- **Resource Creation**: Terraform scripts are used to automate the creation of GCS buckets, BigQuery datasets, and other required GCP resources. This approach ensures consistency and repeatability in setting up the project environment.
## Result
#### our dag in airflow :
![Screenshot](https://github.com/2000aliali/Customer-Churn-Prediction-Project-using-GCP-Terraform-dbt-airflow-and-ML/blob/main/IMAGES/screen%20of%20result/Capture%20d'%C3%A9cran%202024-09-29%20191612.png)
#### in th bigquery
![Screenshot](https://github.com/2000aliali/Customer-Churn-Prediction-Project-using-GCP-Terraform-dbt-airflow-and-ML/blob/main/IMAGES/bq.png)
in the cloud storage
![Screenshot](https://github.com/2000aliali/Customer-Churn-Prediction-Project-using-GCP-Terraform-dbt-airflow-and-ML/blob/main/IMAGES/gs.png)

#### for our dashboards : fell free to visvit this links: https://lookerstudio.google.com/u/0/reporting/8342ae48-032f-4100-b749-79e3c95c548f/page/tEnnC?s=r3vkVXjrVSo
![Screenshot](https://github.com/2000aliali/Customer-Churn-Prediction-Project-using-GCP-Terraform-dbt-airflow-and-ML/blob/main/IMAGES/dash.png)

#### for our interface of Customer Churn Prediction : fell free to visvit this links: https://customer-churn-ali-el-azzaouy.streamlit.app/
![Screenshot](https://github.com/2000aliali/Customer-Churn-Prediction-Project-using-GCP-Terraform-dbt-airflow-and-ML/blob/main/IMAGES/stream.png)


## Conclusion
The **Customer Churn Prediction Project** effectively leverages modern cloud technologies and machine learning to address business challenges related to customer retention. By employing a systematic approach to data extraction, transformation, and modeling, the project aims to provide valuable insights into customer behavior and enhance decision-making for businesses.
