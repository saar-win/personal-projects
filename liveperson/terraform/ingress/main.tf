resource "kubernetes_ingress" "ingress" {
  metadata {
    name = "basic-ingress"
    namespace = "airflow"
  }

  spec {
    backend {
      service_name = "airflow-web"
      service_port = 8080
    }

    rule {
      http {
        path {
          backend {
            service_name = "airflow-web"
            service_port = 8080
          }

          path = "/"
        }
      }
    }
  }
}
output "load_balancer_ip" {
  value = kubernetes_ingress.ingress.status.0.load_balancer.0.ingress.0.ip
}