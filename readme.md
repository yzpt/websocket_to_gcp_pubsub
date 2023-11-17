# websocket extracttion with GCE

## 1. Docker build image

```bash
# build docker image
docker build -t py-gce gce_websocket/

docker images
IMAGE_NAME=py-gce

# run locally
docker run py-gce
```

## 2. Push to GCP Artifact Registry

### 2.2. GCP configuration

```bash
PROJECT_ID=$(gcloud config get-value project)
echo ---- project: $PROJECT_ID

REGION=europe-west9

SERVICE_ACCOUNT_EMAIL=$(gcloud iam service-accounts list --filter="displayName:cryptos-gcp-sa" --format='value(email)')
echo ---- SA:$SERVICE_ACCOUNT_EMAIL

```

### 2.3. Push to GCP Artifact Registry

```bash
APP_LOCAL_FOLDER=gce_websocket
ARTIFACT_REGISTRY_REPO_NAME=ws-gce-yzpt
ARTIFACT_REGISTRY_LOCATION=europe-west9
IMAGE_NAME=py-gce

# Set Artifact Registry administrator permissions for the service account
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" --role="roles/artifactregistry.writer"

# Create a repository on Artifact Registry
gcloud artifacts repositories create $ARTIFACT_REGISTRY_REPO_NAME --repository-format=docker --location=$ARTIFACT_REGISTRY_LOCATION --description="py-websocket container on GCE"

# Docker/GCP Authentication
gcloud auth configure-docker $ARTIFACT_REGISTRY_LOCATION-docker.pkg.dev --quiet

# tag the local docker image
docker tag $IMAGE_NAME $ARTIFACT_REGISTRY_LOCATION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REGISTRY_REPO_NAME/$IMAGE_NAME

# Push Docker to GCP Artifact Registry
docker push $ARTIFACT_REGISTRY_LOCATION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REGISTRY_REPO_NAME/$IMAGE_NAME
echo $ARTIFACT_REGISTRY_LOCATION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REGISTRY_REPO_NAME/$IMAGE_NAME
```

### 2.4. Deploy to GCE

```bash
# Create a GCE instance










