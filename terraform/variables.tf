variable "project_id" {
  description = "The GCP project ID where the resources will be created."
  type        = string
  default     = "seconde-gcp-project"
}

variable "bucket_name" {
  description = "The name of the bucket to create."
  type        = string
  default     = "bucket_dbdata"
}

variable "location" {
  description = "The location for the bucket and PostgreSQL instance."
  type        = string
  default     = "europe-west2"
}

variable "db_instance_name" {
  description = "The name of the PostgreSQL instance to create."
  type        = string
  default     = "dbdata"
}

variable "db_version" {
  description = "The version of PostgreSQL to use."
  type        = string
  default     = "POSTGRES_13"
}

variable "db_password" {
  description = "The password for the PostgreSQL root user."
  type        = string
  sensitive   = true
}
