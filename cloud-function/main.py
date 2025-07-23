import base64
import json
from deploy_to_run import deploy_to_cloud_run

def deploy_app_logic(event, context):
    print("📥 Received Pub/Sub event")

    try:
        # Decode base64 message
        message = base64.b64decode(event['data']).decode('utf-8')
        data = json.loads(message)

        image = data.get("image")
        if image:
            print(f"🚀 Triggering deployment for image: {image}")
            deploy_to_cloud_run("my-app", image)
            print("✅ Deployment triggered successfully.")
        else:
            print("❌ No 'image' found in the message payload.")
            raise ValueError("Missing 'image' key in Pub/Sub message")

    except Exception as e:
        print(f"❌ Error processing Pub/Sub message: {e}")
        raise
