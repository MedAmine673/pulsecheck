# PulseCheck

A developer uptime monitoring service built with **FastAPI**, **SQLModel**, **PostgreSQL**, and **Docker**.

PulseCheck monitors the availability of websites by periodically sending HTTP requests, recording their health status, response time, and history.

The project is built as a backend system that demonstrates real-world practices:

* API development
* Database modeling
* Background workers
* Containerization
* Automated testing
* Production-oriented architecture

---

# Features

## Monitor Management

The API allows users to:

* Add URLs to monitor
* List monitored URLs
* View monitoring history
* Delete monitors

Available endpoints:

| Method | Endpoint                 | Description              |
| ------ | ------------------------ | ------------------------ |
| GET    | `/health`                | Application health check |
| POST   | `/monitors/`             | Add a URL to monitor     |
| GET    | `/monitors/`             | List all monitors        |
| GET    | `/monitors/{id}/history` | Get check history        |
| DELETE | `/monitors/{id}`         | Remove a monitor         |

---

# How It Works

The application has three main components:

```
                HTTP Request
                     |
                     v

              FastAPI Application
                     |
        +------------+-------------+
        |                          |
        v                          v

   PostgreSQL Database        Background Scheduler

        |                          |
        |                          |
        v                          v

 Monitor Data             Website Health Checks

                     |
                     v

              CheckResult History
```

## Scheduler

A background scheduler runs every 60 seconds.

For every monitored URL it:

1. Sends an HTTP request
2. Measures response time
3. Checks HTTP status code
4. Determines if the service is up or down
5. Stores the result in the database

Example stored result:

```json
{
  "status_code": 200,
  "response_time": 145,
  "is_up": true,
  "timestamp": "2026-06-15T10:00:00"
}
```

---

# Tech Stack

| Layer               | Technology     |
| ------------------- | -------------- |
| API                 | FastAPI        |
| ORM                 | SQLModel       |
| Database            | PostgreSQL     |
| Containerization    | Docker         |
| Local orchestration | Docker Compose |
| Testing             | Pytest         |
| Server              | Uvicorn        |

---

# Project Structure

```
pulsecheck/
│
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Database models
│   ├── database.py          # Database connection and sessions
│   ├── scheduler.py         # Background monitoring worker
│   │
│   └── routers/
│       └── monitors.py      # Monitor API endpoints
│
├── tests/
│   └── test_monitors.py     # API tests
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Running Locally With Docker

## Requirements

Install:

* Docker
* Docker Compose

---

## Start the application

Build and run:

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

# Environment Variables

The application uses environment variables for configuration.

Example:

```env
DATABASE_URL=postgresql://user:password@db:5432/pulsecheck
```

The same application code can run with:

* SQLite for development
* PostgreSQL for production

---

# Testing

Run tests:

```bash
pytest
```

The tests verify:

* Creating monitors
* Listing monitors
* Retrieving history
* Handling missing monitors
* Deleting monitors

---

# Database Design

The database contains two main tables:

## Monitor

Stores URLs being monitored.

Example:

```
Monitor
--------
id
url
```

## CheckResult

Stores every health check result.

Example:

```
CheckResult
------------
id
monitor_id
status_code
response_time
timestamp
is_up
```

Relationship:

```
Monitor
   |
   |
   +---- CheckResult
   |
   +---- CheckResult
   |
   +---- CheckResult
```

A monitor can have many historical check results.

---

# Current Architecture

Current development environment:

```
                 Docker Compose

        +---------------------------+
        |                           |
        |                           |
        v                           v

   FastAPI Container          PostgreSQL Container

        |
        |
        v

 Background Scheduler
```

---

# Development Progress

## Phase 1 — Application Core ✅

Completed:

* FastAPI API
* SQLModel database models
* Monitor CRUD operations
* Monitoring scheduler
* Database persistence
* Automated tests

---

## Phase 2 — Dockerization 🚧

Completed:

* Docker image creation
* Docker Compose setup
* PostgreSQL container
* Environment-based configuration

Next:

* Multi-stage Docker build
* Container security improvements
* CI pipeline preparation

---

## Phase 3 — Cloud Deployment (Planned)

Future goals:

* Terraform infrastructure
* Azure Container Apps
* Azure PostgreSQL Flexible Server
* Private networking
* Azure Key Vault
* GitHub Actions CI/CD
* Application Insights monitoring

---

# Goals of the Project

This project is designed to practice building a production-style backend system:

* Designing APIs
* Managing databases
* Containerizing applications
* Deploying cloud infrastructure
* Automating delivery pipelines
* Applying security best practices
