terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  credentials = file("credentials/key.json")
}

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = var.artifact_repository_id
  description   = "Executor Docker Repository"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false
  }
  
  cleanup_policies {
    id     = "delete-all-old"
    action = "DELETE"
    condition {
      tag_state    = "ANY"
      older_than   = "14d"
    }
  }
}

resource "google_cloud_run_v2_service" "recommend_service" {
  name     = "recommend-service"
  location = var.region
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.image_name
      ports {
        name           = "h2c"
        container_port = 50051
      }
    }
    scaling {
      min_instance_count = 0
      max_instance_count = 1
    }
  }
  
}

resource "google_cloud_run_service_iam_binding" "recommend_service" {
  location = google_cloud_run_v2_service.recommend_service.location
  service  = google_cloud_run_v2_service.recommend_service.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}
