import logging
from rq import Queue, Worker, Connection
from redis import Redis, ConnectionPool
import os
import uuid
from multiprocessing import Process

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Redis configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))


# Connect to Redis container
pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
redis_conn_pool = Redis(connection_pool=pool)

# Create a queue
queue = Queue("queue", connection=redis_conn_pool, default_timeout=10, result_ttl=86400)

# Generate a worker ID
def generate_worker_id():
    return str(uuid.uuid4())

# Verify Redis connection
def verify_redis_connection():
    try:
        result = redis_conn_pool.ping()
        if result:
            logging.info("Redis connection verified successfully.")
        else:
            logging.error("Redis connection verification failed.")
    except ConnectionError as e:
        logging.error("Error connecting to Redis: %s", e)

# Worker function
def start_worker():
    with Connection(redis_conn_pool):
        worker_id = generate_worker_id()
        worker = Worker([queue], name=worker_id)
        worker.work()  # Enable burst mode for faster task processing

# Function to create and start multiple worker processes
def start_workers(num_workers):
    processes = []
    for _ in range(num_workers):
        process = Process(target=start_worker)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

if __name__ == '__main__':
    # Verify Redis connection
    verify_redis_connection()
    
    # Specify the number of worker processes you want
    num_workers = 4
    
    # Start the worker processes
    logging.info(f"Starting {num_workers} worker processes...")
    start_workers(num_workers)
