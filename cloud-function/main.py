steps:
  # Step 0: Deploy Cloud Function only if it doesn't exist
  - name: 'gcr.io/cloud-builders/gcloud'
    id: check-function
    entrypoint: bash
    args:
      - -c
      - |
        echo "🔍 Checking if Cloud Function exists...";
        if ! gcloud functions describe deployAppfunction --region=asia-south1 --gen2 > /dev/null 2>&1; then
          echo "☁️ Deploying Cloud Function for the first time...";
          gcloud functions deploy deployAppfunction \
            --gen2 \
            --runtime=python311 \
            --entry-point=deploy_app_logic \
            --region=asia-south1 \
            --source=cloud-function \
            --trigger-topic=deploy-topic \
            --timeout=540s \
            --memory=512MB;
        else
          echo "✅ Cloud Function already exists. Skipping deployment.";
        fi

  # Step 1: Build Docker image from 'app/' directory
  - name: 'gcr.io/cloud-builders/docker'
    dir: 'app'
    args:
      - build
      - -t
      - asia-south1-docker.pkg.dev/$PROJECT_ID/my-repo/my-app:$SHORT_SHA
      - .

  # Step 2: Push Docker image to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - push
      - asia-south1-docker.pkg.dev/$PROJECT_ID/my-repo/my-app:$SHORT_SHA

  # Step 3: Publish to Pub/Sub to trigger Cloud Function
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - pubsub
      - topics
      - publish
      - deploy-topic
      - --message={"image":"asia-south1-docker.pkg.dev/$PROJECT_ID/my-repo/my-app:$SHORT_SHA"}

substitutions:
  _REGION: asia-south1
  _SERVICE_NAME: my-app

options:
  logging: CLOUD_LOGGING_ONLY
