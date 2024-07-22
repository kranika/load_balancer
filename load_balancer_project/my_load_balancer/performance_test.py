import matplotlib.pyplot as plt
import time
import asyncio
import aiohttp

async def send_requests(url, n_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for _ in range(n_requests)]
        responses = await asyncio.gather(*tasks)
        return [response.status for response in responses]

def generate_bar_chart(data, title, x_label, y_label, filename):
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values())
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(filename)
    plt.close()

def generate_line_chart(data, title, x_label, y_label, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(data.keys(), data.values(), marker='o')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(filename)
    plt.close()

async def experiment_A1(base_url):
    n_requests = 10000
    n_servers = 3
    responses = await send_requests(base_url, n_requests)
    server_counts = {f'Server {i+1}': responses.count(200 + i) for i in range(n_servers)}
    generate_bar_chart(server_counts, 'Request Count Handled by Each Server', 'Server', 'Request Count', 'bar_chart.png')
    return server_counts

async def experiment_A2(base_url):
    n_requests = 10000
    server_counts = {}
    for n_servers in range(2, 7):
        responses = await send_requests(base_url, n_requests)
        avg_load = sum([responses.count(200 + i) for i in range(n_servers)]) / n_servers
        server_counts[f'{n_servers} Servers'] = avg_load
    generate_line_chart(server_counts, 'Average Load of Servers', 'Number of Servers', 'Average Load', 'line_chart.png')
    return server_counts

async def experiment_A3(base_url):
    n_requests = 10000
    server_counts = {}
    response_times = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 6):  # Testing with 1 to 5 servers
            start_time = time.time()
            responses = await send_requests(base_url, n_requests)
            end_time = time.time()
            avg_response_time = (end_time - start_time) / n_requests
            response_times.append(avg_response_time)
            server_counts[f'{i} Servers'] = avg_response_time
    generate_line_chart(server_counts, 'Average Response Time per Server Count', 'Number of Servers', 'Average Response Time (s)', 'response_time_chart.png')
    return server_counts

async def experiment_A4(base_url):
    n_requests = 10000
    server_counts = {}
    async with aiohttp.ClientSession() as session:
        for i in range(1, 6):  # Testing with 1 to 5 servers
            responses = await send_requests(base_url, n_requests)
            counts = [responses.count(200 + j) for j in range(i)]
            server_counts[f'{i} Servers'] = sum(counts) / len(counts)
    generate_bar_chart(server_counts, 'Request Distribution per Server Count', 'Number of Servers', 'Average Requests per Server', 'distribution_chart.png')
    return server_counts

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"  # Load balancer URL
    asyncio.run(experiment_A1(base_url))
    asyncio.run(experiment_A2(base_url))
    asyncio.run(experiment_A3(base_url))
    asyncio.run(experiment_A4(base_url))
