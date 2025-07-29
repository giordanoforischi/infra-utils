# Terraform - Cloud NAT Gateway on/off trigger

## Summary

This Terraform/Docker code was created to toggle the creation and destruction of resources in GCP. The resources comprise a network gateway for serverless microservices to use. These services typically operate with random IP addresses and, with the gateway, they can be configured to use the gateway's IP address. This can help in setting up authorized connections to external SQL databases, for example.

The reason why we mount/dismount the gateway is to reduce cost. Its structure generates costs due to virtual machine provisioning, even when idle. By mounting and dismounting the infrastructure we enable it to be scheduled so it is provisioned only in a specific period during the day, in which we operate the outgoing connections from our microservices.

## Usage

- "Secret" folder: this folder contains a sa.json file with a service account key. It should have all the necessary permissions to create and destroy the resources.
- "tf_files" folder: contains the Terraform files that describe the three services used as the gateway: a Cloud Router, Cloud NAT and VPC Access Connector. It is important to add a backend to the provider, so state can be stored outside the runtime of the Docker containers, and accessed by each create/destroy flow remotely. It uses a Cloud Storage bucket for that.
- Dockerfile, yml, .sh files in main folder: The build.bat file builds the Docker contains files and pushes them to GCP. The job_*.yml files define the Cloud Run jobs that are executed to mount/dismount the network infrastructure. The shell files contain the Terraform commands ran when the job is started.
- Use Cloud Scheduler to trigger the moun/dismount jobs.

## Stack

- Terraform
- Docker
- GCP Cloud Run
- GCP Cloud Storage
- GCP Cloud NAT, Router and VPC Access Connector
- GCP Cloud Scheduler