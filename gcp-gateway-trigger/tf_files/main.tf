terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.12.0"
    }
  }

  backend "gcs" {
    bucket = "bd_gateway"
    prefix    = "state"
  }
}

provider "google" {
  /* credentials = file("./sa.json") */
  project = var.project
  region  = var.region
}