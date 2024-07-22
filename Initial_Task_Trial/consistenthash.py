import math

class ServerContainer:
    def __init__(self, id):
        self.id = id
        self.virtual_servers = []

class ConsistentHashMap:
    def __init__(self, num_containers, num_slots):
        self.num_containers = num_containers
        self.num_slots = num_slots
        self.containers = [ServerContainer(i) for i in range(num_containers)]
        self.hash_map = [None] * num_slots

    def H(self, i):
        return (i + 2 * i + 17) % self.num_slots

    def Phi(self, i, j):
        return (i + j + 2 * j + 25) % self.num_slots

    def add_virtual_servers(self, num_virtual_servers):
        for container in self.containers:
            for j in range(num_virtual_servers):
                slot = self.Phi(container.id, j)
                container.virtual_servers.append(slot)
                if self.hash_map[slot] is None:
                    self.hash_map[slot] = container
                else:
                    # Handle collision using linear probing
                    next_slot = (slot + 1) % self.num_slots
                    while self.hash_map[next_slot] is not None:
                        next_slot = (next_slot + 1) % self.num_slots
                    self.hash_map[next_slot] = container

    def map_request_to_container(self, request_id):
        slot = self.H(request_id)
        container = self.hash_map[slot]
        if container is None:
            return None  # No server container found for this request
        else:
            return container.id

# Initialize consistent hash map
num_containers = 3
num_slots = 512
consistent_hash_map = ConsistentHashMap(num_containers, num_slots)

# Add virtual servers to the hash map
num_virtual_servers = math.ceil(math.log2(num_slots))
consistent_hash_map.add_virtual_servers(num_virtual_servers)

# Map requests to server containers
request_id = 123456
container_id = consistent_hash_map.map_request_to_container(request_id)
print("Request", request_id, "is mapped to Server Container", container_id)
