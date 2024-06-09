from flask import Flask, request, jsonify
from redis import Redis, ConnectionError
from rq import Queue, Connection, Worker, Callback
from rq.job import Job
import time
app = Flask(__name__)

# Connect to Redis container
redis_host = "redis"  # Redis service name in Docker Compose network
redis_port = 6379
redis_conn = Redis(host=redis_host, port=redis_port)
queue = Queue("queue",connection=redis_conn, default_timeout=5,  result_ttl=86400)

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

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    job = queue.enqueue('tasks.Process_Login', data)   
    return jsonify({'message': 'login request added to queue ', 'job_id' : str(job.id)})

@app.route('/create_student', methods=['POST'])
def create_student():
    data = request.json
    job = queue.enqueue('tasks.Process_Create', data)   
    return jsonify({'message': 'student creation request added to queue', 'job_id': str(job.id)})

@app.route('/job_status', methods=['POST'])
def job_status():
    data = request.json
    job_id = data['job_id']
    print(job_id)
    job = Job.fetch(job_id, connection=redis_conn)
    result = job.latest_result(timeout=60) 
    result_content = result.return_value
    return jsonify({'status': str(job.get_status()), 'result': str(result_content)})

@app.route('/queue_status', methods=['POST'])
def queue_status():       
    total_queue_count = len(queue) 
    finished_jobs_count = queue.finished_job_registry
    total_finished_jobs= len(finished_jobs_count)
    return jsonify({'total_queue': total_queue_count , 'total_finished_jobs': total_finished_jobs})

@app.route('/worker_status', methods=['POST'])
def worker_status():    
    total_worker_count = len(Worker.all(queue=queue))
    return jsonify({'total_workers': total_worker_count})

if __name__ == '__main__':
    verify_redis_connection(redis_conn)
    app.run(debug=True)


