terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
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
    zone = var.google_zone
    project  = var.project_name
}

data "google_client_config" "default" {
  depends_on = [module.gke-cluster]
}

data "google_container_cluster" "default" {

  name = var.cluster_name
  depends_on = [module.gke-cluster]
}

provider "kubernetes" {
  host  = "https://${data.google_container_cluster.default.endpoint}"
  token = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(
    data.google_container_cluster.default.master_auth[0].cluster_ca_certificate,
  )
}

provider "helm" {
  kubernetes {
    host  = "https://${data.google_container_cluster.default.endpoint}"
    token = data.google_client_config.default.access_token
    cluster_ca_certificate = base64decode(
      data.google_container_cluster.default.master_auth[0].cluster_ca_certificate,
    )
  }
}

module "gke-cluster" {
  source              = "./gke-cluster"
  cluster_name        = var.cluster_name
  google_zone         = var.google_zone
  node_locations      = var.node_locations
  name_space          = var.name_space
  kubernetes_version  = var.kubernetes_version

}

module "kubernetes-config" {
  source              = "./kubernetes-config"
  depends_on          = [module.gke-cluster]
  cluster_name        = var.cluster_name
  name_space          = var.name_space
}