# load_balancer.py

from flask import Flask, jsonify
import os
import hashlib
import docker
from collections import defaultdict

app = Flask(__name__)

# Configuration
N = 3  # Number of replicas
total_slots = 512
K = 9  # Number of virtual servers for each server container
server_replicas = []

# Consistent Hashing
class ConsistentHashing:
    def __init__(self, total_slots, K):
        self.total_slots = total_slots
        self.K = K
        self.hash_ring = defaultdict(list)
        self.servers = []

    def hash_function(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16) % self.total_slots

    def add_server(self, server):
        self.servers.append(server)
        for i in range(self.K):
            virtual_server = f"{server}:{i}"
            hash_value = self.hash_function(virtual_server)
            self.hash_ring[hash_value].append(server)

    def remove_server(self, server):
        self.servers.remove(server)
        for i in range(self.K):
            virtual_server = f"{server}:{i}"
            hash_value = self.hash_function(virtual_server)
            self.hash_ring[hash_value].remove(server)

    def get_server(self, key):
        hash_value = self.hash_function(key)
        sorted_keys = sorted(self.hash_ring.keys())
        for k in sorted_keys:
            if k >= hash_value:
                return self.hash_ring[k][0]
        return self.hash_ring[sorted_keys[0]][0]

# Initialize consistent hashing
consistent_hash = ConsistentHashing(total_slots, K)

# Initialize Docker client
client = docker.from_env()

# Function to start new server
def start_new_server():
    container = client.containers.run(
        "server-image",  # Image name
        environment={"SERVER_ID": len(server_replicas) + 1},
        name=f"server_{len(server_replicas) + 1}",
        network="load_balancer_network",
        detach=True
    )
    return container.name

# Ensure N replicas
while len(server_replicas) < N:
    server_name = start_new_server()
    server_replicas.append(server_name)
    consistent_hash.add_server(server_name)

# Define the /rep endpoint
@app.route('/rep', methods=['GET'])
def get_replicas():
    response = {
        "message": {
            "N": len(server_replicas),
            "replicas": server_replicas
        },
        "status": "successful"
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
