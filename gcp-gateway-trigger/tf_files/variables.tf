variable "project" {
  type        = string
  default     = "PROJECT"
}

variable "region" {
  description = "The region to deploy resources in"
  type        = string
  default     = "us-central1"
}

variable "network" {
  type        = string
  default     = "default-vpc-network" #  "https://www.googleapis.com/compute/v1/projects/etl-directories1/global/networks/default-vpc-network"
}