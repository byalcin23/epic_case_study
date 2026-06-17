# Epic Petstore Case Study

Small Python service for the Swagger Petstore API.

The application fetches pets with `available` status, filters pets whose name starts with `M`, prints the required message, and stores selected records in PostgreSQL.

## Quick Start

```bash
git clone https://github.com/byalcin23/epic_case_study.git
cd epic_case_study
docker compose up
```

No local build is required. The application image is public on Docker Hub:

```text
bahadir23/epic_petstore_api:v002
```

The database uses the official PostgreSQL image:

```text
postgres:15
```

## Run API Tests

The Postman/Newman test suite is under `postman/`.

```bash
docker compose run --rm api-tests
```

The collection covers the Swagger Petstore `/pet` endpoints, including successful requests, status code checks, response validation, invalid requests, and basic negative scenarios.

## Database

PostgreSQL data is stored in a named Docker volume:

```text
postgres-data
```

This keeps the data between normal `up` and `down` runs.

Inspect records:

```bash
docker compose exec db psql -U appuser -d appdb -c "SELECT * FROM pets LIMIT 20;"
```

Check duplicate records:

```bash
docker compose exec db psql -U appuser -d appdb -c "SELECT id, COUNT(*) FROM pets GROUP BY id HAVING COUNT(*) > 1;"
```

No rows returned means no duplicate records.

## Project Structure

- `main.py` - application flow
- `api.py` - Swagger Petstore API call
- `databese.py` - PostgreSQL connection and insert logic
- `postman/` - Postman/Newman API test collection
- `docker-compose.yml` - app, database, network, healthcheck, volume, and API test setup
- `Dockerfile` - image definition used for publishing the app image

## Generic Questions

### 1. Docker vs Kubernetes deployment

Docker Compose is simpler and mostly used for local or small environments. It starts the defined containers on one Docker host.

Kubernetes is a container orchestration platform. From a deployment point of view, it gives better options for scaling, self-healing, rolling updates, service discovery, config management, and running workloads across multiple nodes.

### 2. What problem does Docker Compose solve?

Docker Compose makes it easy to run a multi-container application with one file and one command. In this project, the app, database, network, volume, healthcheck, and API test runner are described in `docker-compose.yml`.

In Kubernetes, the same idea is handled with manifests such as `Deployment`, `Service`, `ConfigMap`, `Secret`, `PersistentVolumeClaim`, and `Job`.

### 3. Logs, metrics, and traces

Logs are application or system events written as text. They are useful for understanding what happened at a specific moment.

Metrics are numeric measurements over time, such as request count, error rate, CPU usage, memory usage, or response time.

Traces show the path of a request across services. They help understand where time is spent and where a request failed in a distributed system.

### 4. Idempotency

Idempotency means running the same operation multiple times has the same final result as running it once.

It is important because deployments, retries, API calls, and database operations can happen more than once. Idempotent behavior makes systems safer and more predictable. In this project, duplicate database records are prevented by using the Petstore `id` as the primary key and `ON CONFLICT (id) DO NOTHING`.

### 5. Production considerations

For production, I would avoid hardcoded database credentials and move them to secrets or environment-specific configuration.

I would also consider:

- using a private or controlled container registry
- adding CI/CD pipeline steps for build, test, scan, and deployment
- improving logging and monitoring
- adding application healthchecks
- running more than one application replica
- using a managed or replicated PostgreSQL setup
- defining backup and restore procedures
- adding reverse proxy or ingress configuration
- setting resource limits and restart policies
- reviewing network access, credentials, and image security
