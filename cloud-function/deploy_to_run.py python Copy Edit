import subprocess

def deploy_to_cloud_run(service_name, image_uri):
    region = "asia-south1"  # Change as needed
    subprocess.run([
        "gcloud", "run", "deploy", service_name,
        "--image", image_uri,
        "--platform", "managed",
        "--region", region,
        "--allow-unauthenticated"
    ])
