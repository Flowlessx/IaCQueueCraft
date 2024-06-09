# app.py

from flask import Flask, request, jsonify
from rq import Queue, Connection, Worker
from rq.exceptions import DequeueTimeout
from rq.serializers import JSONSerializer
from redis import Redis
import os
import time
import sys
import uuid 
import tasks 

app = Flask(__name__)

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

#db_name = os.environ['DB_NAME']
# Connect to Redis container
redis_host = "redis"  # Redis service name in Docker Compose network
redis_port = 6379
redis_conn = Redis(host=redis_host, port=redis_port)

queue = Queue("queue", connection=redis_conn)

def generate_worker_id():
    # Generate a UUID (Universally Unique Identifier) as the worker ID
    return str(uuid.uuid4())

def verify_redis_connection(redis_conn):
    try:
        # Attempt a simple operation on the connection object
        result = redis_conn.ping()
        if result:
            print("Redis connection verified successfully.")
        else:
            print("Redis connection verification failed.")
    except Redis.exceptions.ConnectionError as e:
        print("Error connecting to Redis:", e)

def worker():
    worker_id = generate_worker_id()
    worker = Worker([queue], connection=redis_conn, name=worker_id)
    worker.work()
    try:
        # Assuming redis_conn is defined somewhere in your code
        with Connection(redis_conn):       
            print(f"Worker ID: {worker_id}")
            verify_redis_connection(redis_conn)
            print(f"Redis connected to worker thread : {worker_id}")
            print(redis_conn)
            while True:
                try:
                    time.sleep(5)
                    print("Check Queue for items")
                    print('Successful jobs: ' + str(worker.successful_job_count))
                    print('Failed jobs: ' + str(worker.failed_job_count))
                    print('Total working time: ' + str(worker.total_working_time))  # In seconds
                    #job = queue.lpop("queue", timeout=10)
                except DequeueTimeout:
                    print("Dequeue operation timed out. Retrying...")
                    continue
    except Exception as e:
        print("redis")
        print(e)

if __name__ == '__main__':
    # Start the worker process
    worker()
    app.run(debug=True)
