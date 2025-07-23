import subprocess

def deploy_to_cloud_run(service_name, image_uri):
    try:
        subprocess.run([
            "gcloud", "run", "deploy", service_name,
            "--image", image_uri,
            "--platform", "managed",
            "--region", "asia-south1",
            "--allow-unauthenticated"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ gcloud deployment failed: {e}")
        raise
