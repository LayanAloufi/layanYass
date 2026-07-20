# Todo App

A simple full-stack Todo application built for a DevOps containerization practice task.
You can add, list, and delete todos.

## Stack

- **Frontend:** React (Vite), served by Nginx
- **Backend:** Flask (Python) REST API
- **Database:** PostgreSQL

## Project Structure

```
.
├── backend/                # Flask REST API
│   ├── app.py
│   ├── requirements.txt
├── frontend/               # React app (Vite + Nginx)
│   ├── src/
│   ├── package.json
│   ├── nginx.conf    
└── .env.example            # Sample environment variables
```

## API Endpoints

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/api/health`      | Health check        |
| GET    | `/api/todos`       | List all todos      |
| POST   | `/api/todos`       | Create a todo       |
| DELETE | `/api/todos/<id>`  | Delete a todo by id |

`POST /api/todos` expects a JSON body: `{ "title": "Buy milk" }`.

## Configuration

The backend reads its database configuration from environment variables:

| Variable      | Default     |
| ------------- | ----------- |
| `DB_HOST`     | `localhost` |
| `DB_PORT`     | `5432`      |
| `DB_NAME`     | `todos`     |
| `DB_USER`     | `postgres`  |
| `DB_PASSWORD` | `postgres`  |

Copy `.env.example` to `.env` to override the defaults used by Docker Compose.

## Note 

Frontend dockerfile command to run the application:
CMD ["nginx", "-g", "daemon off;"]

Backend dockerfile command to run the application:

gunicorn command 

## Running with Docker Compose

```bash
use a command to build and run the compose file
```

Then open:

- Frontend: http://localhost:3000
- Backend health check: http://localhost:5000/api/health

# DevOps Practice Task — Docker Compose + CI Image Publishing

## Objective

You are given a simple Todo application with:

* React frontend
* Flask backend
* PostgreSQL database

Your task is to containerize the application, run it using Docker Compose, apply proper Docker networking and volumes, and create a GitHub Actions CI workflow that builds and pushes Docker images to Docker Hub.

---

## Task 1: Create Dockerfiles

Create Dockerfiles for both services:

### Frontend

Requirements:

* Create a `frontend/Dockerfile`.
* Use a multi-stage build.
* Build the React application in the build stage.
* Serve the final frontend using a lightweight runtime image, such as Nginx.
* The final image should only contain the runtime files needed to serve the frontend.

### Backend
Requirements:

* Create a `backend/Dockerfile`.
* Use a clean Python base image.
* Install dependencies from `requirements.txt`.
* Run the Flask application inside the container.
* Apply proper Docker caching by copying dependency files before copying the full source code.

---

## Task 2: Run the Application Manually Using Docker Commands

Before using Docker Compose, run the application manually using normal Docker commands.

The goal of this task is to understand what Docker Compose does behind the scenes.

Requirements:

Build the frontend Docker image manually using docker build.
Build the backend Docker image manually using docker build.
Create the required Docker networks manually using docker network create.
Create the required Docker volume manually using docker volume create.
Run the PostgreSQL container manually using docker run.
Run the backend container manually using docker run.
Run the frontend container manually using docker run.
Use Docker flags such as:
-d
--name
-p
-e
--env-file
--network
-v

Important requirements:

The database container should not expose its port to the host machine.
The backend should be able to connect to the database.
The frontend should be reachable from the host machine.
The frontend should be able to communicate with the backend.
Use a Docker volume to persist PostgreSQL data.
Document all manual Docker commands used in the README.md.

Useful commands to include in the README:

docker build
docker run
docker ps
docker logs
docker exec
docker network create
docker network ls
docker network inspect
docker network connect
docker volume create
docker volume ls
docker volume inspect
docker stop
docker rm

After the manual Docker setup works successfully, move to the next task and convert the same setup into Docker Compose.


## Task 3: Create Docker Compose File

After successfully running the application manually using Docker commands, create a docker-compose.yml file that runs the same setup in a cleaner and easier way.

The Docker Compose file should replace the manual docker run, network, volume, port, and environment variable commands.

Requirements:

* The frontend should be reachable from the host machine.
* The backend should be reachable by the frontend.
* The database should only be reachable by the backend.
* Do not expose the database port to the host machine.
* Use a named volume for PostgreSQL data.
* Use environment variables for database configuration.
* Use at least two custom networks:

  * One network between frontend and backend.
  * One network between backend and database.

Expected network idea:

```text
frontend-net:
  frontend
  backend

db-net:
  backend
  db
```

The frontend should not be connected directly to the database network.

---

## Task 4: Add Environment Configuration

Create an example environment file:

```text
.env.example
```

It should include the required variables, but no real secrets.

Example:

```env
POSTGRES_DB=todo_db
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=change_me
DATABASE_HOST=db
DATABASE_PORT=5432
```

Do not commit real secrets to the repository.

---

## Task 5: Add Docker Hub CI Workflow

Create a GitHub Actions workflow under:

```text
.github/workflows/docker-ci.yml
```

Requirements:

* The workflow should run on:

  * `push`
  * `pull_request`
* On pull requests:

  * Build the frontend Docker image.
  * Build the backend Docker image.
  * Do not push images to Docker Hub.
* On push to the main branch:

  * Build the frontend Docker image.
  * Build the backend Docker image.
  * Push both images to Docker Hub.
* Use GitHub Actions secrets for Docker Hub login.

Required GitHub secrets:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

Suggested image names:

```text
<dockerhub-username>/todo-frontend
<dockerhub-username>/todo-backend
```

Suggested tags:

```text
latest
github-sha
```

Example:

```text
todo-backend:latest
todo-backend:<commit-sha>
```

---

## Task 6: Update README.md

Update the `README.md` with clear instructions.

The README should include:

* Project overview.
* How to build and run the containers manually using Docker commands.
* How to run the project with Docker Compose.
* How to stop the project.
* How to remove containers and volumes.
* Explanation of the Docker networks.
* Explanation of the database volume.
* Explanation of the difference between the manual Docker approach and Docker Compose.
* Explanation of the GitHub Actions workflow.
* Docker Hub image links after the workflow pushes successfully.


Required commands to document:

```bash
docker compose up -d --build
docker compose down
docker compose down -v
docker ps
docker images
docker volume ls
docker network ls
```

---

## Questionnaire

Answer the following questions inside the `README.md`.

### Docker Questions

1. In a multi-stage Dockerfile, why does the final image only contain the final/runtime stage?
   
 **-A multi-stage Dockerfile separates the build environment from the runtime environment. Only the files copied into the final   stage are included in the final image. This keeps the image smaller .**


2. Why is it better to copy dependency files first, install dependencies, and then copy the full source code?
   
 **-If only the application source code changes but the dependency files remain the same, Docker reuses the cached dependency layer instead of reinstalling all dependencies. This significantly speeds up image builds.**


3. What is the difference between a Docker volume and a bind mount?

  **-A Docker volume is managed by Docker and is mainly used to persist application data, such as a database. A bind mount links a specific directory from the host machine to the container, allowing both to share the same files directly.**



### Manual Docker vs Docker Compose Questions

1. What is the benefit of running the containers manually before using Docker Compose?

  **-Running containers manually helps understand how Docker works by learning how to create networks, volumes, environment variables, and containers individually. Docker Compose then automates these steps.**


2. Which `docker run` flags were replaced by the `docker-compose.yml` file?

 **--name**

  **-p (port mapping)**

  **-e (environment variables)**

  **--network**

  **-v (volumes)**

  **These settings are defined once in the docker-compose.yml file.**


3. Why is Docker Compose easier to manage when the project has frontend, backend, and database services?

  -Docker Compose allows all services to be defined in a single file and started with one command. It automatically creates networks, attaches volumes, applies environment variables, and manages communication between services.



### Docker Compose / Networking Questions

1. Why should the database not expose its port to the host machine in this task?

  -The database is only used by the backend service. Keeping it internal improves security by preventing direct access from the host machine or external users.

2. How can the backend connect to the database if the database port is not exposed to the host?

  -Both containers are connected to the same Docker network. The backend connects to the database using the service name 


3. Why do we use separate Docker networks for frontend-backend and backend-database communication?

  -Using separate networks isolates services and limits communication only to containers that need it.



### GitHub Actions Questions

1. What is the difference between running the workflow on `pull_request` and running it on `push` to `main`?

  -On a pull request, the workflow only builds the Docker images to verify that the project builds successfully. On a push to the main branch, the workflow builds the images and then pushes them to Docker Hub.

2. Why should Docker Hub credentials be stored as GitHub Actions secrets?

  -Secrets keep sensitive information secure and prevent usernames and access tokens from being exposed in the repository or workflow files.

3. Why should the workflow build images on pull requests but only push images when code is merged to `main`?

  -Building images during pull requests verifies that the changes do not break the project before merging. Pushing images only after merging to main ensures that only tested and approved code is published to Docker Hub.

---

## Deliverables

Please submit:

* GitHub repository link.
* Screenshot of `docker compose up -d --build` running successfully.
* Screenshot showing the frontend, backend and DB containers running.
* Screenshot of the frontend working in the browser.
* Screenshot of the successful GitHub Actions workflow.
* Docker Hub links for the pushed images.
* Updated `README.md` with commands, explanations, and questionnaire answers.

---

## Acceptance Criteria

The task is complete when:

* Frontend runs successfully in Docker.
* Backend runs successfully in Docker.
* Backend connects successfully to PostgreSQL.
* Database data persists using a named volume.
* Frontend and backend are connected through the correct network.
* Database is isolated and not exposed directly to the host.
* Docker Compose starts the full application with one command.
* GitHub Actions builds the images successfully.
* GitHub Actions pushes images to Docker Hub only from the main branch.
* Secrets are used correctly.
* README is clear and complete.

Deadline: Tuesday, 21 July 2026, 4:00 PM.

After submission, we will review the implementation together. Be ready to explain your Dockerfiles, Docker Compose networks, volumes, and GitHub Actions workflow.



## PROJECT OVERVIEW 
Project Overview
This project is a containerized Todo application built to demonstrate Docker, Docker Compose, and CI/CD concepts. The application consists of three services:
Frontend: A React (Vite) application served with Nginx.
Backend: A Flask REST API that handles todo operations.
Database: A PostgreSQL database used to store todo items persistently.
The project demonstrates how multiple services can communicate through Docker networks, how persistent data is managed using Docker volumes, and how the entire application can be orchestrated with Docker Compose. It also includes a GitHub Actions workflow that automatically builds the Docker images on pull requests and publishes them to Docker Hub when changes are merged into the main branch.

## Build and Run the Containers Manually

 **Build the Backend Image:** 
 
 -docker build -t todo-backend ./backend
 
**Run the Backend Container:**

-docker run -d --name backend -p 5000:5000 todo-backend

**Build the Frontend Image:**

 -docker build -t todo-frontend ./frontend
 
**Run the Frontend Container:**

-docker run -d --name frontend -p 3000:80 todo-frontend

## Run the Project with Docker Compose

-docker compose up -d --build

## Stop the Project

-docker compose down

 ## Remove Containers and Volumes

 -docker compose down -v

 ## Docker Networks 
 
-Docker networks allow containers to communicate.

-The frontend communicates with the backend.

-The backend communicates with PostgreSQL.

-Containers use container names instead of IP addresses.

-Networks isolate services and improve security.


## Database Volume

The project uses a named Docker volume called postgres-data.
The volume stores PostgreSQL data outside the database container.
This ensures that the database contents remain available even if the PostgreSQL container is stopped or removed. When a new PostgreSQL container is created using the same volume, it can continue using the existing data.


## Manual Docker vs Docker Compose

-Running the application manually requires executing multiple Docker commands to build images, create networks, create volumes, and start each container individually. This approach helps understand how Docker works behind the scenes and how containers communicate.

-Docker Compose simplifies this process by defining all services, networks, volumes, ports, and environment variables in a single docker-compose.yml file. Instead of running many commands.


## GitHub Actions Workflow

The workflow runs automatically when code is pushed or when a pull request is opened.
On a pull request, the workflow builds the frontend and backend Docker images to verify that the project builds successfully. The images are not pushed to Docker Hub.

On a push to the main branch, the workflow builds both Docker images, logs in to Docker Hub using GitHub Secrets (DOCKERHUB_USERNAME and DOCKERHUB_TOKEN), and pushes the images with the latest tag and the current commit SHA tag.
This provides an automated CI pipeline that validates changes before merging and publishes updated Docker images only after code is merged into the main branch.


## Docker Hub Images

-Frontend:  https://hub.docker.com/repository/docker/layanaloufi/todo-frontend


-Backend:  https://hub.docker.com/repository/docker/layanaloufi/todo-backend















