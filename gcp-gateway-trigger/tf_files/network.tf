# These are the resources that need to be deleted and recreated daily, so the Cloud Function can run.
resource "google_vpc_access_connector" "connector" {
  name          = "bdgateway-vpcconn"
  ip_cidr_range = "10.8.0.0/28"
  machine_type   = "e2-micro"
  max_instances  = 10
  min_instances  = 2
  region        = var.region
  network       = var.network
}

resource "google_compute_router" "router" {
  name    = "bdgateway-router"
  network = var.network
  project = var.project
  region  = var.region
}

resource "google_compute_router_nat" "nat" {
  name                               = "bdgateway-nat"
  project                            = var.project
  region                             = var.region
  router                             = google_compute_router.router.name
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
  nat_ip_allocate_option             = "MANUAL_ONLY"
  nat_ips                            = ["https://www.googleapis.com/compute/v1/projects/PROJECT/regions/us-central1/addresses/bd-gateway-fixedip"]
}