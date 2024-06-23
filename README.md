![uav-api](https://github.com/YuunsGit/uav-backend/assets/42357900/ef82d82e-3be0-442b-adc6-37445708f3eb)

# UAV API - [api.uav.yunusemre.dev/api](https://api.uav.yunusemre.dev/api/)
The UAV API is a simple yet robust and ready-to-use API designed for managing drones, their tasks, and the images they capture. It is seamlessly integrated with the [UAV Monitoring App](https://github.com/YuunsGit/uav-frontend), providing a streamlined and maintainable workflow. This document provides detailed instructions on installation, configuration, and usage of the UAV API.

- Live preview of the API: [api.uav.yunusemre.dev/api](https://api.uav.yunusemre.dev/api)
- Live preview of the MinIO Web UI: [api.uav.yunusemre.dev/minio](https://api.uav.yunusemre.dev/minio) 

## Prerequisites
Before installing the UAV API, ensure that you have the following prerequisites installed on your system:

- Docker
- Docker Compose

## Installation

1. Clone the repository
   
   ```sh
   git clone https://github.com/YuunsGit/uav-backend.git
   ```

2. Navigate to the project directory and build the Docker containers using Docker Compose:
   
   ```sh
   cd uav-backend
   docker compose build
   ```

3. Rename the `.env.example` file to `.env` in the root directory of the project

4. Run the docker container with compose
   
   ```sh
   docker compose up --watch
   ```

## Endpoints
The API has the following endpoints:

| Method | Endpoint                | Description             | URL                                                                 |
|--------|-------------------------|-------------------------|---------------------------------------------------------------------|
| GET    | /api/drones             | Get all drones          | https://api.uav.yunusemre.dev/api/drones                            |
| GET    | /api/drones/:id         | Get drone details       | https://api.uav.yunusemre.dev/api/drones/2                          |
| GET    | /api/tasks              | Get all tasks           | https://api.uav.yunusemre.dev/api/tasks                             |
| POST   | /api/tasks              | Create a task           | https://api.uav.yunusemre.dev/api/tasks                             |
| POST   | /api/tasks/:id          | Get task details        | https://api.uav.yunusemre.dev/api/tasks/2                           |
| POST   | /api/tasks/:id/execute  | Execute a task          | https://api.uav.yunusemre.dev/api/tasks/2/execute                   |
| GET    | /api/tasks/:id/images   | Get images of a task    | https://api.uav.yunusemre.dev/api/tasks/2/images                    |
| GET    | /api/images/:id         | Get an image            | https://api.uav.yunusemre.dev/api/images/1429847415                 |

## Docker
The UAV API uses Docker and Docker Compose for containerization, ensuring consistent environments across different development and production setups. Below are the main components defined in the compose.yml file:

- uav-api: The main API service running the Flask application.
- minio: An object storage server compatible with Amazon S3 APIs.

## Stack:

- **<ins>Python</ins>** as programming language
- **<ins>Flask</ins>** as micro web framework
- **<ins>SQLite</ins>** for relational database
- **<ins>SQLAlchemy</ins>** for ORM
- **<ins>MinIO</ins>** for object storage
- **<ins>Pillow</ins>** for image generation
- **<ins>Azure VM</ins>** for API deployment
- **<ins>Nginx</ins>** for reverse proxy

## Postman collection:
To test the UAV API endpoints, you can use the provided Postman collection. Click the button below to import the collection into your Postman workspace:

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/19399613-7619162a-c6e5-4d94-b7a3-711ac350a92f?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D19399613-7619162a-c6e5-4d94-b7a3-711ac350a92f%26entityType%3Dcollection%26workspaceId%3Dbdd9bb4d-c525-4497-98bc-762f0704a207#?env%5BUAV%20Monitoring%5D=W3sia2V5IjoiYXBpX3VybCIsInZhbHVlIjoiaHR0cDovLzEyNy4wLjAuMTo1MDAwL2FwaSIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0In0seyJrZXkiOiJ0YXNrX2lkIiwidmFsdWUiOiIxIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQifSx7ImtleSI6ImRyb25lX2lkIiwidmFsdWUiOiIxIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQifSx7ImtleSI6ImltYWdlX2lkIiwidmFsdWUiOiIxIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQifV0=)

