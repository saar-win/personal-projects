resource "kubernetes_namespace" "airflow" {
 metadata {
   name = "airflow"
 }
}

resource "helm_release" "airflow" {
  name       = "airflow"
  repository = "https://airflow-helm.github.io/charts"
  chart      = "airflow"
  version    = var.chart_version
  namespace  = var.namespace
  wait       = false

  values = [file("${path.module}/helm_values/values.yaml")]

  set {
    name  = "ingress.web.annotations.kubernetes\\.io/ingress\\.class"
    value = var.ingress_class
  }

  set {
    name  = "ingress.flower.annotations.kubernetes\\.io/ingress\\.class"
    value = var.ingress_class
  }

  set {
    name  = "airflow.config.AIRFLOW__GOOGLE__CLIENT_ID"
    value = var.google_oauth_client_id
  }

  set {
    name  = "airflow.config.AIRFLOW__GOOGLE__CLIENT_SECRET"
    value = var.google_oauth_client_secret
  }

}