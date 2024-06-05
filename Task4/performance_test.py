import requests
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()
    
    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(10000):
                task = asyncio.ensure_future(fetch(session, 'http://localhost:5000/home'))
            task.append(task)
            responses = await asyncio.gather(*tasks)
            
        #Analyze responses
server_counts = {}
for response in responses:
    server_id = response['message'].split(": ")[1]
    if server_id not in server_counts:
        server_counts[server_id] = 0
        server_counts[server_id] += 1
        print(server_counts)

    asyncio.run(main())