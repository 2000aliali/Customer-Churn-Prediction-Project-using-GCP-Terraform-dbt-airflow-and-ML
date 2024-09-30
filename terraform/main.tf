# Provider configuration for Google Cloud
provider "google" {
  credentials = file("path/to/data-ali-project-2024-4e14676a6135.json")  # Replace with your service account key
  project     = "your-gcp-project-id"  # Replace with your GCP project ID
  region      = "europe-west2"  # Set to europe-west2
}

# Create a Google Cloud Storage bucket
resource "google_storage_bucket" "bucket_dbdata" {
  name     = "bucket_dbdata"  # Replace with your bucket name
  location = "EUROPE-WEST2"
  storage_class = "STANDARD"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 365
    }
  }
}

# Create a BigQuery dataset in europe-west2
resource "google_bigquery_dataset" "dataset_bank" {
  dataset_id = "dataset_bank"
  location   = "EUROPE-WEST2"
}

# Create Cloud Composer Environment with minimal configuration
resource "google_composer_environment" "composer_environment" {
  name   = "my-composer-environment"  # Name your Composer environment
  region = "europe-west2"

  config {
    software_config {
      image_version   = "composer-3-airflow-2.9.3-build.0"
      python_version  = "3"

      # Specify DAGs folder in Cloud Storage
      dag_gcs_prefix  = "gs://${google_storage_bucket.bucket_dbdata.name}/dags"
    }

    # Use the minimal resources configuration as provided
    node_config {
      service_account = "49974941217-compute@developer.gserviceaccount.com"
      network         = "default"  # Assuming you're using the default network
    }

    workloads_config {
      scheduler {
        count       = 1
        cpu         = 0.5
        memory_gb   = 2
        storage_gb  = 1
      }
      dag_processor {
        count       = 1
        cpu         = 1
        memory_gb   = 2
        storage_gb  = 1
      }
      triggerer {
        count       = 1
        cpu         = 0.5
        memory_gb   = 1
        storage_gb  = 1
      }
      web_server {
        cpu         = 0.5
        memory_gb   = 2
        storage_gb  = 1
      }
      worker {
        min_count   = 1
        max_count   = 3
        cpu         = 0.5
        memory_gb   = 2
        storage_gb  = 10
      }
    }

    # Other config options (default)
    env_variables = {
      "GOOGLE_CLIENT_ID" = "your-client-id"
    }
  }
}

# Optionally, enable Cloud Composer's web server access control to allow access from all IPs
resource "google_composer_environment" "composer_env_with_web_access" {
  depends_on = [google_composer_environment.composer_environment]

  config {
    web_server_access_control {
      allowed_ip_ranges {
        value = "0.0.0.0/0"
      }
    }
  }
}
