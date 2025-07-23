# deploy_to_run.py
import base64
import subprocess

def deploy_app_logic(event, context):
    data = base64.b64decode(event['data']).decode('utf-8')
    image_uri = eval(data)['image']
    print(f"Triggering Cloud Run deployment for image: {image_uri}")
    
    subprocess.run([
        "gcloud", "run", "deploy", "my-app",
        "--image", image_uri,
        "--platform", "managed",
        "--region", "asia-south1",
        "--allow-unauthenticated"
    ], check=True)
