# Medallion Architecture datasets

resource "google_bigquery_dataset" "bronze" {
  project     = var.project_id
  dataset_id  = "bronze"
  description = "Bronze layer for raw ingested market data"
  location    = var.region
}

resource "google_bigquery_dataset" "silver" {
  project     = var.project_id
  dataset_id  = "silver"
  description = "Silver layer for cleaned and structured market data"
  location    = var.region
}

resource "google_bigquery_dataset" "gold" {
  project     = var.project_id
  dataset_id  = "gold"
  description = "Gold layer for analytical market data"
  location    = var.region
}

# Tables

resource "google_bigquery_table" "bronze_market_klines" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.bronze.dataset_id
  table_id   = "market_klines"

  description = "Bronze market kline messages from Pub/Sub subscription"

  deletion_protection = false

  schema = jsonencode([
    {
      name        = "data"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Raw Pub/Sub message data"
    },
    {
      name        = "attributes"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Flattened Pub/Sub attributes"
    },
    {
      name        = "message_id"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Pub/Sub message ID"
    },
    {
      name        = "publish_time"
      type        = "TIMESTAMP"
      mode        = "NULLABLE"
      description = "Time when the message was published to Pub/Sub"
    },
    {
      name        = "subscription_name"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Name of the subscription that wrote this row"
    }
  ])
}

# Scheduled quey

resource "google_bigquery_data_transfer_config" "bronze_to_silver" {
  project                = var.project_id
  display_name           = "bronze_to_silver_hourly"
  location               = var.region
  data_source_id         = "scheduled_query"
  destination_dataset_id = google_bigquery_dataset.silver.dataset_id
  schedule               = "every 1 hours"

  #schedule_options {
  # start_time = "2026-05-31T21:00:00Z"
  # }

  service_account_name = google_service_account.bq_schedule_sa.email
  params = {
    destination_table_name_template = "market_klines"
    write_disposition               = "WRITE_TRUNCATE"
    query                           = file("${path.module}/../app/bq_scripts/bronze_to_silver.sql")
  }
}

# View

resource "google_bigquery_table" "silver_missing_klines" {
  dataset_id = google_bigquery_dataset.silver.dataset_id
  table_id   = "vw_missing_klines"

  deletion_protection = false

  view {
    query          = file("${path.module}/../app/bq_scripts/vw_missing_klines_silver.sql")
    use_legacy_sql = false
  }
}