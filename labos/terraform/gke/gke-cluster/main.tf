terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.52"
    }
  }
}

data "google_compute_zones" "available" {
}

data "google_container_engine_versions" "supported" {
  location       = var.google_zone
  version_prefix = var.kubernetes_version
}

resource "google_container_cluster" "default" {
  name               = var.cluster_name
  location           = var.google_zone
  initial_node_count = var.workers_count
  min_master_version = data.google_container_engine_versions.supported.latest_master_version
  node_version       = data.google_container_engine_versions.supported.latest_master_version

  node_locations = [var.node_locations]

  node_config {
    machine_type = var.machine_type

    oauth_scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}
