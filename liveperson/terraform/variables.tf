variable "cluster_name" {
  type = string
}
variable "google_zone" {
  type = string
}
variable "node_locations" {
  type = string
}
variable "workers_count" {
  type = number
}
variable "name_space" {
  type = string
}
variable "kubernetes_version" {
  type = string
}
variable "project_name" {
  type = string
}
variable "ingress_service_name" {
  type = string
}
variable "ingress_port" {
  type = number
}
variable "service_port" {
  type = number
}
variable "service_name" {
  type = string
}
variable "machine_type" {
  type = string
}
