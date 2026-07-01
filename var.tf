variable "project_id" {
  type        = string
  description = "Google Cloud Project ID"
  default     = "plated-client-499118-m4" # Aapka actual live project ID
}

variable "region" {
  type        = string
  description = "UK Regional Deployment Area"
  default     = "europe-west2" # UK Region
}

variable "zone" {
  type        = string
  description = "GKE Node Availability Zone"
  default     = "europe-west2-a"
}