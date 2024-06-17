# Load Balancer Projects
This is a customised load balancer that is part of a class assignment

### Overview of Each Task
#### Task 1: Setting Up the Initial Environment

*Purpose:*
The first task focused on setting up the initial environment for the load balancer and server instances. This involved creating a Docker Compose configuration that defines multiple services, ensuring they can communicate within a shared network.

*Key Steps:*
1. *Docker Compose Setup*:
    - Created a docker-compose.yml file that defines the services: server_1, server_2, server_3, and the load_balancer.
    - Configured each server service to run a simple Flask application.
    - Ensured all services are connected to a common network (load_balancer_network).

2. *Flask Application for Server Instances*:
    - Developed a basic Flask application that runs on each server instance.
    - Each server instance responds to a heartbeat request to indicate it is alive and operational.

*Outcome:*
This setup provides a scalable environment where new server instances can be added or removed dynamically, with a load balancer managing the distribution of requests.

#### Task 2: Implementing Load Balancer Endpoints

*Purpose:*
The second task involved implementing RESTful endpoints in the load balancer to manage the server instances. This allows for scaling up or down the number of server instances based on the load or maintenance requirements.

*Key Steps:*
1. **GET /rep Endpoint**:
    - Implemented an endpoint that returns the list of currently running server instances.
    - The load balancer queries Docker to list containers with names starting with server_.

2. **GET /heartbeat Endpoint**:
    - Implemented a heartbeat endpoint to check if the load balancer itself is running.

3. **POST /add Endpoint**:
    - Developed an endpoint to add new server instances.
    - Validates the request payload to ensure the number of hostnames does not exceed the number of instances to be added.
    - Starts new Docker containers based on the specified or randomly assigned hostnames.

*Outcome:*
These endpoints provide the necessary API to interact with the load balancer for adding new servers and querying the current state of the server instances.

#### Task 3: Implementing Server Removal Endpoint

*Purpose:*
The third task focused on implementing an endpoint to remove server instances, allowing for scaling down based on decreased demand or during maintenance.

*Key Steps:*
1. **DELETE /rm Endpoint**:
    - Developed an endpoint to remove server instances.
    - Validates the request payload to ensure the list of hostnames does not exceed the number of instances to be removed.
    - Removes the specified server instances or randomly selects instances for removal if no specific hostnames are provided.

2. *Validation and Error Handling*:
    - Ensured that appropriate error messages and status codes are returned for invalid requests (e.g., when the list of hostnames is longer than the number of instances to be removed).

*Outcome:*
This endpoint completes the load balancer functionality by providing the ability to remove server instances, making the system adaptable to changing load conditions and maintenance needs.

### Overall Purpose

The combined tasks establish a dynamic and scalable load balancing system using Docker and Flask. The load balancer can scale server instances up or down based on the system's requirements, ensuring efficient resource utilization and high availability. By managing server instances dynamically, the system can maintain optimal performance and reliability, adapting to varying client demands and operational conditions.
