import base64
import json
import subprocess

def deploy_app_logic(event, context):
    print("📥 Received Pub/Sub event")

    try:
        # Decode the event payload
        data = base64.b64decode(event['data']).decode('utf-8')
        payload = json.loads(data)

        image_uri = payload.get("image")
        if not image_uri:
            raise ValueError("No 'image' field found in Pub/Sub message.")

        print(f"🚀 Deploying to Cloud Run with image: {image_uri}")

        # Trigger the Cloud Run deployment
        subprocess.run([
            "gcloud", "run", "deploy", "my-app",
            "--image", image_uri,
            "--platform", "managed",
            "--region", "asia-south1",
            "--allow-unauthenticated"
        ], check=True)

        print("✅ Deployment completed.")

    except Exception as e:
        print(f"❌ Error during deployment: {e}")
        raise
