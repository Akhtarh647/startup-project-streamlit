resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "movie-analytics-repo"
  description   = "Docker Repository for Streamlit Startup App"
  format        = "DOCKER"
}