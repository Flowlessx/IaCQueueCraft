import os
import time
from redis import Redis, ConnectionPool
from rq import Queue, Worker
from kubernetes import client, config
from rq.serializers import JSONSerializer
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log to a file
)

# Create a logger
logger = logging.getLogger(__name__)

# Connect to Redis container
_redis_host = os.environ['REDIS_HOST']
_redis_port = os.environ['REDIS_PORT']

pool = ConnectionPool(host=_redis_host, port=_redis_port, decode_responses=False)
redis_conn = Redis(connection_pool=pool)

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
    print(total_items)
    return total_items

def scale_worker_deployment(namespace, deployment_name, num_workers):
    print(f"Scaling Workers to {num_workers}")
    try:
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
        
    except Exception as e:
        logger.critical(e)


if __name__ == "__main__":
    print("Started Scaler")
    namespace = "prod-worker"  # Replace with your namespace
    deployment_name = "worker-deployment"  # Replace with your deployment name
    print('Started Scaler')
    while True:    
        total_worker_count = len(Worker.all(queue=queue))  
        queue_length = get_queue_length()
        desired_num_workers = 1
        
        # Check queue length
        if queue_length > 100:
            desired_num_workers = (queue_length // 100) + 1
        elif queue_length > 1000:
            desired_num_workers = (queue_length // 100) * 2
        
        # Do not scale workers higher as 80
        if desired_num_workers > 20:
            desired_num_workers = 20    

        print("desired worker: " + str(desired_num_workers))

        if desired_num_workers != total_worker_count:
            scale_worker_deployment(namespace, deployment_name, desired_num_workers)
        time.sleep(60)  # Wait for 30 seconds before checking the queue length again
        
        
