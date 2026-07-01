terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  backend "gcs" {
    bucket = "bucket647" # Aapka secure remote storage bucket
    prefix = "terraform/state/streamlit-app"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}