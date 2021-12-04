terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.3"
    }
    google = {
      source  = "hashicorp/google"
      version = "3.52"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.1.0"
    }
  }
}

provider "google" {
  zone    = var.region
  project = var.project_id
}

data "google_client_config" "default" {
  depends_on = [module.gke-cluster]
}

data "google_container_cluster" "default" {

  name       = var.name
  depends_on = [module.gke-cluster]
}

provider "kubernetes" {
  host  = "https://${data.google_container_cluster.default.endpoint}"
  token = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(data.google_container_cluster.default.master_auth[0].cluster_ca_certificate,
  )
}

provider "helm" {
  kubernetes {
    host                   = "https://${data.google_container_cluster.default.endpoint}"
    token                  = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(data.google_container_cluster.default.master_auth[0].cluster_ca_certificate)
  }
}

module "gke-cluster" {
  source               = "./gke-cluster"
  project_id           = var.project_id
  name                 = var.name
  region               = var.region
  zones                = var.zones
  service_account      = var.service_account
  min_count            = var.min_count
  max_count            = var.max_count
  disk_size_gb         = var.disk_size_gb
  machine_type         = var.machine_type
}
module "airflow" {
  source = "./airflow"
}
module "ingress" {
  source = "./ingress"
}