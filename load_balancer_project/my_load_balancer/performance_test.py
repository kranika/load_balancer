# performance_test.py
import requests
import time
import matplotlib.pyplot as plt

# Configurations
N = 3
num_requests = 10000
load_balancer_url = 'http://localhost:5000/home'

def send_requests():
    start_times = []
    end_times = []
    server_count = {}
    for _ in range(num_requests):
        start_time = time.time()
        response = requests.get(load_balancer_url)
        end_time = time.time()
        server = response.json().get('message', '').split()[-1]
        if server in server_count:
            server_count[server] += 1
        else:
            server_count[server] = 1
        start_times.append(start_time)
        end_times.append(end_time)
    return server_count, start_times, end_times

def plot_results(server_count, start_times, end_times):
    # Bar graph for load distribution
    servers = list(server_count.keys())
    counts = list(server_count.values())
    plt.figure(figsize=(10, 5))
    plt.bar(servers, counts, color='blue')
    plt.xlabel('Servers')
    plt.ylabel('Number of Requests')
    plt.title('Load Distribution among Servers')
    plt.show()

    # Line chart for request handling times
    handling_times = [end - start for start, end in zip(start_times, end_times)]
    plt.figure(figsize=(10, 5))
    plt.plot(range(num_requests), handling_times, color='red')
    plt.xlabel('Request Number')
    plt.ylabel('Handling Time (seconds)')
    plt.title('Request Handling Times')
    plt.show()

if __name__ == '__main__':
    server_count, start_times, end_times = send_requests()
    plot_results(server_count, start_times, end_times)
