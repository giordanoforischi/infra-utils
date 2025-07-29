# GCP authentication commands

#### To set the user account
```bash
gcloud config set account {user_id}
```

#### To login
```bash
gcloud auth login
```

#### To login to ADC
```bash
gcloud auth application-default login
```

#### To set the user account
```bash
gcloud config set project {project_id}
```

#### To set the ADC quota project
```bash
gcloud auth application-default set-quota-project {project_id}
```

#### To set the default Cloud Run region
```bash
gcloud config set run/region us-central1
```

#### To set artifact registry repository
```bash
gcloud config set artifacts/repository LIBRARY_AR
```