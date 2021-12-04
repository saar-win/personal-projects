# terraform {
#   required_providers {
#     google = {
#       source  = "hashicorp/google"
#       version = "3.52"
#     }
#   }
# }
# data "google_container_engine_versions" "supported" {
#   location       = var.google_zone
#   version_prefix = var.kubernetes_version
# }


# resource "google_container_cluster" "default" {
#   name               = var.cluster_name
#   location           = var.google_zone
#   initial_node_count = var.workers_count
#   min_master_version = data.google_container_engine_versions.supported.latest_master_version
#   node_version       = data.google_container_engine_versions.supported.latest_master_version

#   node_locations = [var.node_locations]

#   node_config {
#     machine_type = var.machine_type

#     oauth_scopes = [
#       "https://www.googleapis.com/auth/compute",
#       "https://www.googleapis.com/auth/devstorage.read_only",
#       "https://www.googleapis.com/auth/logging.write",
#       "https://www.googleapis.com/auth/monitoring",
#     ]
#   }
# }
data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

module "gke" {
  source                     = "terraform-google-modules/kubernetes-engine/google"
  project_id                 = var.project_id
  name                       = var.name
  region                     = var.region
  zones                      = var.zones
  network                    = "default"
  subnetwork                 = ""
  ip_range_pods              = ""
  ip_range_services          = ""
  http_load_balancing        = false
  network_policy             = false
  horizontal_pod_autoscaling = true
  remove_default_node_pool   = true

  node_pools = [
    {
      name                      = "default-node-pool"
      service_account           = "${var.service_account}"
      machine_type              = "${var.machine_type}"
      min_count                 = "${var.min_count}"
      max_count                 = "${var.max_count}"
      disk_size_gb              = "${var.disk_size_gb}"
      disk_type                 = "pd-standard"
      image_type                = "COS"
      local_ssd_count           = 0
      node_locations            = ""
      auto_repair               = true
      auto_upgrade              = true
      preemptible               = false
    },
  ]

  node_pools_oauth_scopes = {
    all = []

    default-node-pool = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  node_pools_labels = {
    all = {}

    default-node-pool = {
      default-node-pool = true
    }
  }

  node_pools_metadata = {
    all = {}

    default-node-pool = {
      node-pool-metadata-custom-value = "my-node-pool"
    }
  }

  node_pools_taints = {
    all = []

    default-node-pool = [
      {
        key    = "default-node-pool"
        value  = true
        effect = "PREFER_NO_SCHEDULE"
      },
    ]
  }

  node_pools_tags = {
    all = []

    default-node-pool = [
      "default-node-pool",
    ]
  }
}