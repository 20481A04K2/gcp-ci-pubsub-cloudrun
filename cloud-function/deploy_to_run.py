from google.cloud import build_v1

def deploy_to_cloud_run(service_name, image_uri):
    try:
        build_client = build_v1.CloudBuildClient()

        build_config = {
            "steps": [
                {
                    "name": "gcr.io/cloud-builders/gcloud",
                    "args": [
                        "run", "deploy", service_name,
                        "--image", image_uri,
                        "--platform", "managed",
                        "--region", "asia-south1",
                        "--allow-unauthenticated"
                    ]
                }
            ]
        }

        project_id = "sylvan-hydra-464904-d9"
        operation = build_client.create_build(project_id=project_id, build=build_config)
        print(f"✅ Triggered Cloud Build for deploying {service_name} with image {image_uri}")
    
    except Exception as e:
        print(f"❌ Cloud Build API call failed: {e}")
        raise
