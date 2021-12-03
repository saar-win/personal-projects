 module "cluster" {
    source             = "./gke-cluster"
    project_id         = var.project_id
    name               = var.name
    region             = var.region
    zones              = var.zones
    service_account    = var.service_account
    min_count          = var.min_count
    max_count          = var.max_count
    disk_size_gb       = var.disk_size_gb
    initial_node_count = var.initial_node_count
    machine_type       = var.machine_type
}