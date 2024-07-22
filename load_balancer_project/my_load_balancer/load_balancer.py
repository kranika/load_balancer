# load_balancer.py
import hashlib
import json
import os
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Consistent hashing setup
N = 3
M = 512
K = 9

servers = []
hash_ring = [None] * M

def hash_function(key):
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % M

def add_server(server_id):
    for i in range(K):
        virtual_node_id = f"{server_id}-{i}"
        hash_index = hash_function(virtual_node_id)
        while hash_ring[hash_index] is not None:
            hash_index = (hash_index + 1) % M
        hash_ring[hash_index] = server_id
    servers.append(server_id)

def remove_server(server_id):
    global servers
    servers = [s for s in servers if s != server_id]
    for i in range(M):
        if hash_ring[i] == server_id:
            hash_ring[i] = None

def get_server_for_key(key):
    hash_index = hash_function(key)
    while hash_ring[hash_index] is None:
        hash_index = (hash_index + 1) % M
    return hash_ring[hash_index]

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"N": len(servers), "replicas": servers}), 200

@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.json
    n = data['n']
    hostnames = data.get('hostnames', [])
    for i in range(n):
        server_id = hostnames[i] if i < len(hostnames) else f"Server-{len(servers) + 1}"
        add_server(server_id)
    return jsonify({"message": {"N": len(servers), "replicas": servers}, "status": "successful"}), 200

@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.json
    n = data['n']
    hostnames = data.get('hostnames', [])
    for i in range(n):
        server_id = hostnames[i] if i < len(hostnames) else random.choice(servers)
        remove_server(server_id)
    return jsonify({"message": {"N": len(servers), "replicas": servers}, "status": "successful"}), 200

@app.route('/<path:path>', methods=['GET'])
def proxy_request(path):
    server_id = get_server_for_key(path)
    # Proxy the request to the selected server
    # This part requires additional setup to forward the request
    return jsonify({"message": f"Proxied to {server_id}"}), 200

if __name__ == '__main__':
    for i in range(N):
        add_server(f"Server-{i + 1}")
    app.run(host='0.0.0.0', port=5000)
