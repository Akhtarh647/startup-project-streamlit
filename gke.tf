resource "google_container_cluster" "primary" {
  name     = "startup-analysis-cluster"
  location = var.zone

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Initial config setup
  remove_default_node_pool = true
  initial_node_count       = 1

  ip_allocation_policy {} # Enforces VPC-native cluster distribution
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "gke-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = 2

  node_config {
    preemptible  = true # Cost-effective strategy for test/dev setups
    machine_type = "e2-medium" # 2 vCPUs, 4GB RAM - perfect for holding csv in memory

    labels = {
      env = "production"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}