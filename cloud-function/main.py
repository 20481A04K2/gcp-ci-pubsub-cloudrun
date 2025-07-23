import base64
import json
from google.cloud.devtools import cloudbuild_v1  # ✅ FIXED: correct import

def deploy_app_logic(event, context):
    print("📥 Received Pub/Sub event")
    try:
        message = base64.b64decode(event['data']).decode('utf-8')
        data = json.loads(message)
        image = data.get("image")
        if not image:
            raise ValueError("Missing 'image' key in Pub/Sub message")

        print(f"🚀 Triggering deployment for image: {image}")
        build_client = cloudbuild_v1.CloudBuildClient()
        build = {
            "steps": [{
                "name": "gcr.io/cloud-builders/gcloud",
                "args": [
                    "run", "deploy", "my-app",
                    "--image", image,
                    "--region", "asia-south1",
                    "--platform", "managed",
                    "--allow-unauthenticated"
                ]
            }]
        }
        build_client.create_build(project_id="sylvan-hydra-464904-d9", build=build)
        print("✅ Deployment triggered successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
