variable "kubernetes_version" {
  type = string
}
variable "workers_count" {
  default = 3
  type = number
}
variable "cluster_name" {
  type = string
}
variable "google_zone" {
  type = string
}
variable "node_locations" {
  type = string
}
variable "name_space" {
  type = string
}
variable "machine_type" {
  type = string
}