
credentials         = "/etc/releai/keys/saar-cluster.json"
project_id          = "snappy-sight-332507"
region              = "europe-west3"
zones               = ["europe-west3-a"]
name                = "gke-cluster"
machine_type        = "n1-standard-4"
min_count           = 1
max_count           = 3
disk_size_gb        = 10
service_account     = "888996088256-compute@developer.gserviceaccount.com"
initial_node_count  = 3