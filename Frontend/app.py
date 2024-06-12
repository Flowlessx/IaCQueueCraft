from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# ENV variables for backend connection
_backend_host = os.environ['BACKEND_HOST']
_backend_port = os.environ['BACKEND_PORT']
_backend_conn_url = f"{_backend_host}:{_backend_port}"

@app.route('/')
def index():
    return render_template('index.html', show_modal=True, total_queue=0, finished_workers=0, finished_jobs=0)

@app.route('/register_company', methods=['POST'])
def register_company():
    data = request.json
    response = requests.post(_backend_conn_url + '/register_company', json=data)
    if response.status_code == 200:
        return jsonify({'message': 'Company registered successfully'  + str(response)})
    else:
        return jsonify({'message': 'Failed to register company' + str(response)}), response.status_code

@app.route('/get_companies', methods=['GET'])
def get_companies():
    response = requests.get(_backend_conn_url + '/get_companies')
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Failed to load companies'}), response.status_code

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    response = requests.post(_backend_conn_url + '/create_account', json=data)
    if response.status_code == 200:
        return jsonify({'message': 'Account created successfully'})
    else:
        return jsonify({'message': 'Failed to create account'}), response.status_code

@app.route('/get_accounts', methods=['POST'])
def get_accounts():
    data = request.json
    response = requests.post(_backend_conn_url + '/get_accounts', json=data)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Failed to load accounts'}), response.status_code

@app.route('/get_account_resources', methods=['POST'])
def get_account_resources():
    data = request.json
    response = requests.post(_backend_conn_url + '/get_account_resources', json=data)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Failed to load account resources'}), response.status_code

@app.route('/queue_status', methods=['GET'])
def queue_status():
    response = requests.get(_backend_conn_url + '/queue_status')
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Failed to fetch queue status'}), response.status_code

@app.route('/worker_status', methods=['GET'])
def worker_status():
    response = requests.get(_backend_conn_url + '/worker_status')
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'message': 'Failed to fetch worker status'}), response.status_code

if __name__ == '__main__':
    print("Frontend started")
    app.run(host='0.0.0.0', port=5001)
