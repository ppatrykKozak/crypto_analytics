# Market Data Analytics Pipeline

Engineering thesis project focused on collecting, processing and organizing financial market data from an external API using Google Cloud Platform.

The project is currently in progress. At this stage, it includes an ingestion stack, Terraform-based cloud infrastructure definitions, Python scripts for data collection, BigQuery SQL scripts and an initial Cloud Run Job structure prepared for future analytical processing.

## Architecture overview

The project follows a simplified Medallion Architecture approach:

- **Bronze layer** - raw market data stored close to the original source format.
- **Silver layer** - curated and cleaned data prepared for further analysis.
- **Gold layer** - planned analytics layer for reporting, statistical calculations and market structure analysis.

Pub/Sub is used as a messaging middleware between the data ingestion component and downstream processing. It helps decouple the Python ingestion script from the rest of the pipeline.

## Technologies

- Python
- SQL
- Google Cloud Platform
- BigQuery
- Pub/Sub
- Compute Engine
- Cloud Run Jobs
- Docker
- Terraform
- Shell script

## Current features

- External API data ingestion scripts
- Streaming data collection script
- Initial historical backfill script structure for loading past market data
- BigQuery SQL scripts for raw-to-curated data transformation
- SQL view for detecting missing market data intervals
- Terraform-based cloud infrastructure definition
- Compute Engine VM configuration
- Startup script template for VM environment setup
- Pub/Sub configuration as messaging middleware
- Initial Cloud Run Job structure prepared for future analytical processing

## Data flow

```text
External API
    ↓
Python ingestion script on Compute Engine VM
    ↓
Pub/Sub messaging middleware
    ↓
BigQuery Bronze layer / raw data
    ↓
SQL transformation
    ↓
BigQuery Silver layer / curated data
    ↓
Planned Gold analytics layer