import base64
import json
from deploy_to_run import deploy_to_cloud_run

def deploy_app_logic(event, context):
    message = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(message)
    image = data.get("image")

    if image:
        deploy_to_cloud_run("my-app", image)
    else:
        print("❌ No image found in the message payload.")
