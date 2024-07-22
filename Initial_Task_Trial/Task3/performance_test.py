import requests
import asyncio
import aiohttp
import matplotlib.pyplot as plt
import os
import random
import time

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main(url, request_count):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for _ in range(request_count)]
        responses = await asyncio.gather(*tasks)
    return responses

def run_test(url, request_count):
    responses = asyncio.run(main(url, request_count))
    server_counts = {}
    for response in responses:
        server_id = response['message'].split(": ")[1]
        if server_id not in server_counts:
            server_counts[server_id] = 0
        server_counts[server_id] += 1
    return server_counts

def plot_bar_chart(data, title, xlabel, ylabel, filename=None):
    plt.bar(data.keys(), data.values())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def plot_line_chart(data, title, xlabel, ylabel, filename=None):
    plt.plot(list(data.keys()), list(data.values()), marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def start_new_server():
    # Function to start a new server container (implementation dependent)
    os.system("docker-compose up -d --scale server=4")

def stop_server(container_name):
    # Function to stop a server container (implementation dependent)
    os.system(f"docker stop {container_name}")

if __name__ == '__main__':
    url = 'http://localhost:5000/home'
    request_count = 10000

    # Test A-1
    server_counts = run_test(url, request_count)
    plot_bar_chart(server_counts, 'Request Count Handled by Each Server', 'Server ID', 'Request Count', filename='bar_chart.png')

    # Test A-2
    avg_loads = {}
    for N in range(2, 7):
        os.system(f"docker-compose up -d --scale server={N}")
        time.sleep(5)  # Give some time for the containers to initialize
        server_counts = run_test(url, request_count)
        avg_load = sum(server_counts.values()) / N
        avg_loads[N] = avg_load
    plot_line_chart(avg_loads, 'Average Load of Servers', 'Number of Servers', 'Average Load', filename='line_chart.png')

    # Test A-3: Handling server failure and recovery
    server_counts_before_failure = run_test(url, request_count)
    plot_bar_chart(server_counts_before_failure, 'Request Count Before Failure', 'Server ID', 'Request Count', filename='before_failure.png')

    # Simulate server failure
    failed_server = random.choice(list(server_counts_before_failure.keys()))
    stop_server(f"task3_server_{failed_server}_1")
    print(f"Server {failed_server} stopped.")
    
    time.sleep(5)  # Allow some time for the system to stabilize
    
    server_counts_after_failure = run_test(url, request_count)
    plot_bar_chart(server_counts_after_failure, 'Request Count After Failure', 'Server ID', 'Request Count', filename='after_failure.png')

    # Start a new server to recover
    start_new_server()
    time.sleep(5)  # Allow some time for the new server to initialize

    # Test again after recovery
    server_counts_after_recovery = run_test(url, request_count)
    plot_bar_chart(server_counts_after_recovery, 'Request Count After Recovery', 'Server ID', 'Request Count', filename='after_recovery.png')

    # Test A-4: Modify hash functions and repeat tests
    # Ensure the consistenthash.py file has the modified hash functions

    # Run test with modified hash functions
    server_counts_mod_hash = run_test(url, request_count)
    plot_bar_chart(server_counts_mod_hash, 'Request Count Handled by Each Server with Modified Hash', 'Server ID', 'Request Count', filename='bar_chart_mod_hash.png')

    avg_loads_mod_hash = {}
    for N in range(2, 7):
        os.system(f"docker-compose up -d --scale server={N}")
        time.sleep(5)  # Give some time for the containers to initialize
        server_counts = run_test(url, request_count)
        avg_load = sum(server_counts.values()) / N
        avg_loads_mod_hash[N] = avg_load
    plot_line_chart(avg_loads_mod_hash, 'Average Load of Servers with Modified Hash', 'Number of Servers', 'Average Load', filename='line_chart_mod_hash.png')
