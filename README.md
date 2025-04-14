# 🎟️ Online Event Ticketing System

An advanced Online Event Ticketing System that enables users to seamlessly browse, book, and manage event tickets. Designed for organizers to create and manage events, and for attendees to easily purchase tickets and track their bookings.

## Prerequisites

Ensure the following tools are installed on your machine before proceeding:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone git@github.com:degisew/event_ticketing_fastapi.git
cd event_ticketing_fastapi
```

### 2. Create a `.env` File

Create a `.env` file in the root of your project directory. This file will contain environment variables for the database and pgAdmin4. Here's an example `.env` file:

```bash
# pgAdmin4
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=<your-pgadmin-password>
```

Make sure to replace `<your-pgadmin-password>` with strong, secure values.

### 3. Build and Run the Containers

Use Docker Compose to build and spin up the containers:

```bash
docker-compose up --build
```

This command will build and run the containers for:

- **PostgreSQL** (as a database backend)
- **pgAdmin4** (To manage the PostgreSQL database)
- **FastAPI application** (An API server)

### 4. Access the Services

- **FastAPI API**: Open your browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to access the FastAPI API docs.

- **pgAdmin4**: Go to [http://localhost:8001](http://localhost:8001) to access pgAdmin4. Use the credentials from your `.env` file to log in.

  - **Email**: `PGADMIN_DEFAULT_EMAIL` from the `.env` file (e.g., `admin@example.com`)
  - **Password**: `PGADMIN_DEFAULT_PASSWORD` from the `.env` file

### 5. Managing PostgreSQL in pgAdmin

Once you're logged in to pgAdmin4, follow these steps to add the PostgreSQL server:

1. Click on "Add New Server".
2. Under the **General** tab, set a name for the server (e.g., `event DB`).
3. Under the **Connection** tab, enter the following details:
   - **Host**: `db` (this is the service name defined in the `docker-compose.yml` file)
   - **Port**: `5432`
   - **Username**: `POSTGRES_USER` from the `.env` file (e.g., `XgkJUcqxEw`)
   - **Password**: `POSTGRES_PASSWORD` from the `.env` file

Click **Save** to add the server, and you should now be able to manage the `waga` database from pgAdmin.

## Project Structure

```bash
├── alembic/               # Alembic migrations Configurations
├── docker
│     └── dev/          
│          └── Dockerfile # FastAPI API Dockerfile for development environment
├── src/                  # Custom Apps collection
├── docs/                 # Documentation files
├── scripts/              # Custom scripts
├── .env                  # Environment variables (you will create this)
├── compose.yaml          # Docker Compose configuration file
└── README.md             # This README file
```

## Useful Docker Commands

Here are some helpful commands to manage the Docker environment:

- **Stop all running containers**:

  ```bash
  docker-compose down
  ```

- **Rebuild and restart containers**:

  ```bash
  docker-compose up --build
  ```

- **Check logs for a specific service**:

  ```bash
  docker-compose logs <service-name>
  ```

  For example:

  ```bash
  docker-compose logs api
  ```

- **Access a running container**:

  ```bash
  docker exec -it <container_name> /bin/bash
  ```

  For example, to access the FastAPI API container:

  ```bash
  docker exec -it <api-container-name> /bin/bash
  ```

## Troubleshooting

- **FastAPI server not reachable**: Ensure the FastAPI app is running on `0.0.0.0` and bound to port 8000 (this is handled by the Docker setup).
- **Database connection errors**: Verify that the database credentials in the `.env` file are correct, and that the PostgreSQL service is up and healthy.

## Volumes

The `docker-compose.yml` file defines two Docker volumes:

- `event_ticket_fastapi_db_data`: Stores the PostgreSQL database data.
- `event_ticket_fastapi_pgadmin_data`: Stores pgAdmin4 configuration data.

These volumes ensure that your data persists across container restarts.
