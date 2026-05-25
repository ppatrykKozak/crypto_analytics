# Market Data Analytics Pipeline

Engineering thesis project focused on collecting, processing and organizing financial market data from an external API using Google Cloud Platform.

The project is currently in progress and focuses on building an ingestion stack, cloud infrastructure and SQL-based data processing layers for further analytics and reporting.

## Technologies

- Python
- SQL
- Google Cloud Platform
- BigQuery
- Cloud Run Jobs
- Compute Engine
- Pub/Sub
- Docker
- Terraform

## Features

- External API data ingestion scripts
- Historical data backfill script
- Streaming data collection script
- Cloud Run Job for cloud-based processing
- BigQuery SQL scripts for raw-to-curated data transformation
- SQL view for detecting missing market data intervals
- Terraform-based cloud infrastructure definition
- Dockerized processing component

## Project structure

The repository contains an `ingestion_stack` module with application code, SQL scripts and infrastructure definitions:

- `ingestion_stack/app/bq_scripts` - BigQuery SQL scripts for data transformation and validation
- `ingestion_stack/app/cloud_run_job_scripts` - Dockerized Cloud Run Job application code
- `ingestion_stack/app/vm_scripts` - Python scripts for data backfill and streaming ingestion
- `ingestion_stack/scripts` - startup script template for VM configuration
- `ingestion_stack/terraform` - Terraform configuration for GCP resources

## Project type

Engineering thesis project developed for academic purposes.

## Status

In progress.
