# Market Data Analytics Pipeline

Engineering thesis project focused on collecting, processing and organizing financial market data from an external API using Google Cloud Platform.

The project is currently in progress. At this stage, it includes an ingestion stack, Terraform-based cloud infrastructure definitions, Python scripts for data collection and SQL scripts for preparing data processing layers.

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
- Initial Cloud Run Job structure prepared for future analytical processing
- BigQuery SQL scripts for raw-to-curated data transformation
- SQL view for detecting missing market data intervals
- Terraform-based cloud infrastructure definition

## Project structure

The repository contains an `ingestion_stack` module with application code, SQL scripts and infrastructure definitions:

- `ingestion_stack/app/bq_scripts` - BigQuery SQL scripts for data transformation and validation
- `ingestion_stack/app/cloud_run_job_scripts` - initial Cloud Run Job structure with Dockerfile and placeholder Python entry point
- `ingestion_stack/app/vm_scripts` - Python scripts for data backfill and streaming ingestion
- `ingestion_stack/scripts` - startup script template for VM configuration
- `ingestion_stack/terraform` - Terraform configuration for GCP resources

## Planned development

- Implement analytical processing in the Cloud Run Job
- Prepare final datasets for reporting and analysis
- Add selected statistical and market structure calculations
- Extend the pipeline with an analytics layer

## Project type

Engineering thesis project developed for academic purposes.

## Status

In progress.
