# GCP build commands

#### To set the project
```bash
gcloud config set project PROJECT
```

#### To auth to ADC quota project
```bash
gcloud auth application-default set-quota-project project
```

#### To replace a Cloud Run YAML configuration
```bash
gcloud run services replace ./service.yaml
```

#### To push a local image to the AR repository (has to have the same name)
```bash
docker push us-central1-docker.pkg.dev/PROJECT/FOLDER/DOCKER_IMG_NAME:latest
```