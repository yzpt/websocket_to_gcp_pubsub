# venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask
pip install kafka-python
pip install websocket-client
pip install google-cloud-pubsub

pip freeze > websocket_app/requirements.txt

# Run the app and redirect logs to a file
cd websocket_app
flask run

# gcloud config
PROJECT_ID="cryptos-gcp"
REGION=europe-west9
SERVICE_ACCOUNT_EMAIL=$(gcloud iam service-accounts list --filter="displayName:cryptos-gcp-sa" --format='value(email)')
echo ---- SA:$SERVICE_ACCOUNT_EMAIL

# get json key
gcloud iam service-accounts keys create keys/key-gcloud.json --iam-account=$SERVICE_ACCOUNT_EMAIL

# === Pub/Sub ===

# Enable Pub/Sub API
gcloud services enable pubsub.googleapis.com

# IAM permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT_EMAIL \
    --role roles/pubsub.admin

TOPIC_NAME="cryptos-streaming"

# Create a Pub/Sub topic
gcloud pubsub topics create $TOPIC_NAME 

# List Pub/Sub topics
gcloud pubsub topics list

# Delete a Pub/Sub topic
gcloud pubsub topics delete $TOPIC_NAME

# List subscriptions
gcloud pubsub subscriptions list

# Create a Pub/Sub subscription
gcloud pubsub subscriptions create $TOPIC_NAME-sub --topic $TOPIC_NAME

# Delete a subscription
gcloud pubsub subscriptions delete $TOPIC_NAME-sub

# display messages
gcloud pubsub subscriptions pull $TOPIC_NAME-sub --auto-ack --limit=100