import os
import random
import docker
from flask import Flask, jsonify, request

app = Flask(__name__)

N = 3
client = docker.from_env()
network_name = "load_balancer_network"  # Ensure this matches the network name in docker-compose.yml

def start_new_server():
    server_id = random.randint(1000, 9999)
    container_name = f"server_{server_id}"
    container = client.containers.run(
        "server-image",
        name=container_name,
        environment={"SERVER_ID": server_id},
        network=network_name,
        detach=True
    )
    return container_name

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = []
    for container in client.containers.list():
        if container.name.startswith("server_"):
            replicas.append(container.name)
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

if __name__ == '__main__':
    for _ in range(N):
        start_new_server()
    app.run(host='0.0.0.0', port=5000)
