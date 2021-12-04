resource "helm_release" "airflow" {
  name       = "airflow"
  namespace  = "airflow"
  chart      = "airflow"
  repository = "https://airflow-helm.github.io/charts"
}
