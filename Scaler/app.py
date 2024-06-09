import os
import time
from redis import Redis
from rq import Queue
from kubernetes import client, config
from rq.serializers import JSONSerializer

# Connect to Redis container
redis_host = "redis"  # Redis service name in Docker Compose network
redis_port = 6380
redis_conn = Redis(host=redis_host, port=redis_port, decode_responses=False)
queue = Queue("queue", connection=redis_conn)

def verify_redis_connection(redis_conn):
    try:
        # Attempt a simple operation on the connection object
        result = redis_conn.ping()
        if result:
            print(result)
            print("Redis connection verified successfully.")
        else:
            print("Redis connection verification failed.")
    except Redis.exceptions.ConnectionError as e:
        print("Error connecting to Redis:", e)

def get_queue_length():
    total_items = queue.count
    return total_items

def scale_worker_deployment(namespace, deployment_name, num_workers):
    print(f"Scaling Workers to {num_workers}")
    # Load kube config
    config.load_incluster_config()  # use load_kube_config() if running outside the cluster
    # Create Kubernetes API client
    apps_v1 = client.AppsV1Api()
    
    # Fetch the current deployment
    deployment = apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
    
    # Update the number of replicas
    deployment.spec.replicas = num_workers
    
    # Apply the updated deployment
    apps_v1.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

if __name__ == "__main__":
    current_num_workers = 0  # Initial number of workers
    namespace = "prod-scaler"  # Replace with your namespace
    deployment_name = "scaler-deployment"  # Replace with your deployment name
    
    while True:
        queue_length = get_queue_length()
        if queue_length > 25:
            desired_num_workers = (queue_length // 25) + 1
        elif queue_length > 1000:
            desired_num_workers = (queue_length // 1000) + 3
        else:
            desired_num_workers = 3  # Minimum number of workers
        
        if desired_num_workers != current_num_workers:
            scale_worker_deployment(namespace, deployment_name, desired_num_workers)
            current_num_workers = desired_num_workers
        
        time.sleep(30)  # Wait for 30 seconds before checking the queue length again
