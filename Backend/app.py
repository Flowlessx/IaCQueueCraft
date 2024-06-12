from flask import Flask, request, jsonify, render_template
from redis import Redis, ConnectionPool
from rq import Queue, Worker, Connection
from rq.job import Job
from gevent.pywsgi import WSGIServer
import os

app = Flask(__name__)

# Redis configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))


# Connection Pool
pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
redis_conn_pool = Redis(connection_pool=pool)

# Queue setup
queue = Queue("queue", connection=redis_conn_pool, default_timeout=10, result_ttl=86400)

@app.route('/')
def index():
    return render_template('index.html', show_modal=True, total_queue=0, finished_workers=0, finished_jobs=0)

# Register company endpoint
@app.route('/register_company', methods=['POST'])
def register_company():
    data = request.json
    job = queue.enqueue('tasks.register_company', data)
    return jsonify({'message': 'Company registration request added to queue', 'job_id': job.id})

# Get companies endpoint
@app.route('/get_companies', methods=['GET'])
def get_companies():
    job = queue.enqueue('tasks.get_companies')
    result = job.latest_result(timeout=60)  #  returns Result(id=uid, type=SUCCESSFUL)
    final_result = result.return_value
    return jsonify({'message': final_result, 'job_id': job.id})

# Create account endpoint
@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    job = queue.enqueue('tasks.create_account', data)
    return jsonify({'message': 'Account creation request added to queue', 'job_id': job.id})

# Get accounts endpoint
@app.route('/get_accounts', methods=['POST'])
def get_accounts():
    data = request.json
    job = queue.enqueue('tasks.get_accounts', data)
    result = job.latest_result(timeout=60)  #  returns Result(id=uid, type=SUCCESSFUL)
    final_result = result.return_value
    return jsonify({'message': final_result, 'job_id': job.id})

# Get account resources endpoint
@app.route('/get_account_resources', methods=['POST'])
def get_account_resources():
    data = request.json
    job = queue.enqueue('tasks.get_account_resources', data)
    return jsonify({'message': 'Get account resources request added to queue', 'job_id': job.id})

# Job status endpoint
@app.route('/job_status', methods=['POST'])
def job_status():
    job_id = request.json.get('job_id')
    job = Job.fetch(job_id, connection=redis_conn_pool)
    result = job.result
    return jsonify({'message': result})

# Queue status endpoint
@app.route('/queue_status', methods=['GET'])
def queue_status():
    total_queue_count = len(queue)
    total_finished_jobs = len(queue.finished_job_registry)
    return jsonify({'total_queue': total_queue_count, 'total_finished_jobs': total_finished_jobs})

# Worker status endpoint
@app.route('/worker_status', methods=['GET'])
def worker_status():
    total_worker_count = len(Worker.all(queue=queue))
    return jsonify({'total_workers': total_worker_count})

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
