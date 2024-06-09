from flask import Flask, render_template, request, jsonify
import requests
from redis import Redis, ConnectionError
from rq import Queue, Connection, Worker, Callback
from rq.serializers import JSONSerializer
from rq.job import Job
from gevent.pywsgi import WSGIServer
app = Flask(__name__)

#db_name = os.environ['DB_NAME']
_frontend_host = 'http://frontend:'
_frontend_port = str(5001)
_backend_host = 'http://backend:'
_backend_port = str(5000)
_frontend_conn_url = _frontend_host +_frontend_port
_backend_conn_url = _backend_host + _backend_port

@app.route('/')
def index():
    return render_template(
        'index.html'   
    )

@app.route('/login', methods=['POST'])
def login():
    data = request.json 
    response = requests.post( _backend_conn_url+ '/login', json=data)
    if response.status_code == 200:
        job_id = response.json().get('job_id')  # Extract job_id from the response
        if job_id:
            # Call job_status endpoint with the job_id
            job_status_response = requests.post( _frontend_conn_url + '/job_status', json={'job_id': job_id})
            if job_status_response.status_code == 200:
                job_data = job_status_response.json()
                if job_data['message']:
                    return jsonify({'message': job_data['message']})
                else:
                    return jsonify({'message': "in progress"}), 202
            else:
                return jsonify({'message': 'Failed to fetch job status'}), job_status_response.status_code
        else:
            return jsonify({'message': 'Job ID not found in response'}), 500
    else:
        return jsonify({'message': 'Failed to execute tests'}), response.status_code


@app.route('/create_student', methods=['POST'])
def create_student():
    data = {
        "student_name": "JohnDoe",
        "student_type": "Regular",
        "student_version": "1.0",
        "student_owner": "JaneSmith",
        "student_password": "securepassword"
    }
    response = requests.post(_backend_conn_url + '/create_student', json=data)
    if response.status_code == 200:
        job_id = response.json().get('job_id')  # Extract job_id from the response
        if job_id:
            # Call job_status endpoint with the job_id
            job_status_response = requests.post(_frontend_conn_url + '/job_status', json={'job_id': job_id})
            if job_status_response.status_code == 200:
                job_data = job_status_response.json()
                if job_data['message']:
                    return jsonify({'message': job_data['message']})
                else:
                    return jsonify({'message': "Student creation in progress"}), 202
            else:
                return jsonify({'message': 'Failed to fetch job status'}), job_status_response.status_code
        else:
            return jsonify({'message': 'Job ID not found in response'}), 500
    else:
        return jsonify({'message': 'Failed to create student'}), response.status_code

@app.route('/job_status', methods=['POST'])
def job_status():
    data = request.json
    job_id = data['job_id']
    if not job_id:
        return jsonify({'message': 'Job ID is required'}), 400
    response = requests.post( _backend_conn_url +'/job_status', json={'job_id': job_id})

    if response.status_code == 200:
        job_data = response.json()
        if job_data['status']:
            return jsonify({'message': job_data['result']})
        else:
            return jsonify({'message': "in progress"}), 202
    else:
        return jsonify({'message': 'Failed to fetch job status'}), response.status_code

@app.route('/queue_status', methods=['POST'])
def queue_status():  
    response = requests.post(_backend_conn_url +'/queue_status')

    if response.status_code == 200:        
        if response.json():
            return jsonify({'message': response.json()})
        else:
            return jsonify({'message': "in progress"}), 202
    else:
        return jsonify({'message': 'Failed to fetch job status'}), response.status_code

@app.route('/worker_status', methods=['POST'])
def worker_status():  
    response = requests.post(_backend_conn_url +'/worker_status')

    if response.status_code == 200:        
        if response.json():
            return jsonify({'message': response.json()})
        else:
            return jsonify({'message': "in progress"}), 202
    else:
        return jsonify({'message': 'Failed to fetch job status'}), response.status_code

if __name__ == '__main__':
    print("frontend started")
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
