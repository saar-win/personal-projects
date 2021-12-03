variable "namespace" {
  type    = string
  default = "airflow"
}
variable "chart_version" {
  type    = string
  default = "6.9.1"
}
variable "ingress_class" {}

variable "google_oauth_client_id" {}
variable "google_oauth_client_secret" {}