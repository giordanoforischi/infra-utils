# gcloud auth configure-docker us-central1-docker.pkg.dev -q

docker build -f Dockerfile.mount -t us-central1-docker.pkg.dev/PROJECT/docker-bdgateway/bdgateway-mount:latest .
docker build -f Dockerfile.dismount -t us-central1-docker.pkg.dev/PROJECT/docker-bdgateway/bdgateway-dismount:latest .

docker push us-central1-docker.pkg.dev/PROJECT/docker-bdgateway/bdgateway-mount:latest
docker push us-central1-docker.pkg.dev/PROJECT/docker-bdgateway/bdgateway-dismount:latest

gcloud run jobs replace ./job_mount.yml
gcloud run jobs replace ./job_dismount.yml