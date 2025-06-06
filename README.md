# Event Ticket Reservation

<div align="center">

<!-- ![Project Logo](https://via.placeholder.com/150x150/0066cc/ffffff?text=LOGO) -->

**A scalable event ticket booking platform built with modern backend technologies**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-brightgreen.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://docker.com)

**Contact**: [degisew.mengist21@gmail.com](mailto:degisew.mengist21@gmail.com) | [LinkedIn](https://linkedin.com/in/degisew-mengist)

</div>

## Overview

An advanced Online Event Ticketing System that enables users to seamlessly browse, book, and manage event tickets. Designed for organizers to create and manage events, and for attendees to easily purchase tickets and track their bookings.

**Key Features**:

- Secure JWT authentication and role-based access control.
- Containerized deployment with Docker.
- Background task processing with FastAPI BackgroundTask.
- QR code ticket generation and sending them through email.
- Ticket booking before payment with expiration time.

<!-- **Links**:

- **Portfolio**: [Portfolio](https://degisew-portfolio.netlify.com)
- **GitHub**: [GitHub](https://github.com/degisew)
- **LinkedIn**: [LinkedIn](https://linkedin.com/in/degisew-mengist) -->

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [API Reference](#api-reference)
- [Architecture](#architecture)
  <!-- - [Testing](#testing) -->
- [Deployment](#deployment)

## Quick Start

```bash
# Clone the repo
git clone https://github.com/degisew/event_ticketing_fastapi.git
cd event_ticketing_fastapi

# Run with Docker
docker-compose up --build

# OR run locally
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements/dev.txt
fastapi dev main.py
```

**Access**: [http://localhost:8000](http://localhost:8000) for API, [http://localhost:8000/docs](http://localhost:8000/docs) for API docs.

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

## Setup

<details>
<summary><strong>Show Setup Details</strong></summary>

### Prerequisites

- Python 3.10+
- Docker 20.10+ & Docker Compose 1.29+
- PostgreSQL 14+ (for local setup)
- Git 2.30+

### Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/degisew/event_ticketing_fastapi.git
   cd event_ticketing_fastapi
   ```

2. **Configure Environment**:

   ```bash
   Create a .env file with-in your root project directory and store secure values.
   ```

   Example `.env`:

   ```bash
   # Database
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=your_db_name

   # FastAPI
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256

   # Optional: pgAdmin
   PGADMIN_DEFAULT_EMAIL=admin@example.com
   PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
   ```

3. **Run the Application**:
   - **Docker (Recommended)**:

     ```bash
     docker-compose up --build
     ```

   - **Local Development**:

     ```bash
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements/dev.txt
     fastapi dev main.py
     ```

4. **Access Services**:
   - API: [http://localhost:8000](http://localhost:8000)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - pgAdmin (if included): [http://localhost:8001](http://localhost:8001)

</details>

## API Reference

<details>
<summary><strong>Show API Reference</strong></summary>

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/account/users` | POST | Register a new user |
| `/api/v1/account/users/profile/edit` | PATCH | Update current user profile |
| `/api/v1/events` | GET | List all events |
| `/api/v1/events` | POST | Create a new event |
| `/api/v1/events/{id}/reservations` | POST | Reserve a ticket for a specific event |
| `/api/v1/reservations/{id}/payments` | POST | Create Payment for a current user reservations|
| `/api/v1/reservations/me` | GET | Get all reservations for a current user|
| `/api/v1/event/{id}/ticket_types` | GET | List all available ticket types for a specific event |

**Full Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

</details>

## Architecture

**Tech Stack**:

- **Backend**: FastAPI for RESTful APIs
- **Database**: PostgreSQL
- **DevOps**: Docker, Docker-compose

<!-- ## Testing

<details>
<summary><strong>Show Testing Details</strong></summary>

```bash
# Run tests With coverage
docker compose exec api pytest

- 85%+ test coverage with `pytest` and `coverage.py`.
- Includes unit tests (models, utilities) and integration tests (API endpoints).
```

</details> -->

## Deployment

<details>
<summary><strong>Show Deployment Details</strong></summary>

### Production

```bash

# Run with Docker Compose
docker-compose -f compose.prod.yaml up -d
```

### Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
```

</details>

## License

MIT License. See [LICENSE](LICENSE).

<div align="center">

**⭐ Star this repo if you found it useful!**

Built by [Degisew Mengist](https://github.com/degisew)

[⬆ Back to Top](#event-ticket-reservation)

</div>
