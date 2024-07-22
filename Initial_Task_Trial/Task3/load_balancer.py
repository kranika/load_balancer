import os
import random
import docker
from flask import Flask, jsonify, request

app = Flask(__name__)

N = 3
client = docker.from_env()
network_name = "task3_load_balancer_network"  

def start_new_server(container_name=None):
    server_id = random.randint(1000, 9999)
    container_name = container_name if container_name else f"server_{server_id}"
    try:
        container = client.containers.run(
            "server-image",
            name=container_name,
            environment={"SERVER_ID": server_id},
            network=network_name,
            detach=True
        )
        return container_name
    except docker.errors.APIError as e:
        print(f"Error starting container {container_name}: {e}")
        return None

def remove_server(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return True
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")
        return False
    except docker.errors.APIError as e:
        print(f"Error removing container {container_name}: {e}")
        return False

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = [container.name for container in client.containers.list() if container.name.startswith("server_")]
    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200

@app.route('/add', methods=['POST'])
def add_server():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    
    if not isinstance(n, int) or n <= 0:
        return jsonify({"message": "Invalid number of instances to add.", "status": "failure"}), 400
    
    if len(hostnames) > n:
        return jsonify({"message": "Mismatch in number of hostnames and instances to add.", "status": "failure"}), 400
    
    for i in range(n):
        container_name = hostnames[i] if i < len(hostnames) else None
        start_new_server(container_name)
    
    replicas = [container.name for container in client.containers.list() if container.name.startswith("server_")]
    
    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.json
    n = data.get('n', 0)
    hostnames = data.get('hostnames', [])
    
    if not isinstance(n, int) or n <= 0:
        return jsonify({"message": "Invalid number of instances to remove.", "status": "failure"}), 400
    
    if len(hostnames) > n:
        return jsonify({"message": "Mismatch in number of hostnames and instances to remove.", "status": "failure"}), 400
    
    replicas = [container.name for container in client.containers.list() if container.name.startswith("server_")]
    
    if len(replicas) <= n:
        return jsonify({"message": "Cannot remove all replicas.", "status": "failure"}), 400
    
    removal_candidates = hostnames + [c for c in replicas if c not in hostnames][:n - len(hostnames)]
    
    for container_name in removal_candidates:
        remove_server(container_name)
    
    replicas = [container.name for container in client.containers.list() if container.name.startswith("server_")]
    
    response = {
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    valid_endpoints = ["home"]
    if path not in valid_endpoints:
        return jsonify({
            "message": f"<Error> '/{path}' endpoint does not exist in server replicas",
            "status": "failure"
        }), 400
    
    request_id = hash(path)  # Using path hash to map to a server container
    container_name = random.choice([c.name for c in client.containers.list() if c.name.startswith("server_")])
    
    if container_name is None:
        return jsonify({
            "message": "<Error> No server container found for this request",
            "status": "failure"
        }), 500
    
    # Simulating request forwarding to the mapped container
    return jsonify({
        "message": f"Request to '/{path}' routed to {container_name}",
        "status": "successful"
    }), 200

if __name__ == '__main__':
    for _ in range(N):
        start_new_server()
    app.run(host='0.0.0.0', port=5000)
