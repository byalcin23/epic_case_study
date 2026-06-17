# Epic Petstore Case Study

Small Python service for the Swagger Petstore API.

The app fetches pets with `available` status, keeps the ones whose name starts with `M`, prints the required message, and stores the selected records in PostgreSQL.

## Images

- Database: `postgres:15` from the official Docker Hub repository
- App: `bahadir23/epic_petstore_api:v002` from my public Docker Hub repository

No local image build is required. The project can be started directly with Docker Compose.

## Run

```bash
docker compose up
```

The app waits until PostgreSQL is healthy before starting.

## API Tests

The Postman/Newman test suite is under `postman/`.

Run it with:

```bash
docker compose run --rm api-tests
```

The collection covers the `/pet` endpoints from the Swagger Petstore API, including successful requests, status code checks, response checks, invalid requests, and basic negative scenarios.

## What It Stores

The `pets` table contains:

- `id`
- `name`
- `status`
- `pet_category`
- `name_character_count`

Duplicate records are prevented by using the Petstore `id` as the primary key.

## Database

PostgreSQL data is stored in a named Docker volume:

```text
postgres-data
```

This keeps the database data between normal `up` / `down` runs.

To inspect the data:

```bash
docker compose exec db psql -U appuser -d appdb -c "SELECT * FROM pets LIMIT 20;"
```

To check duplicates:

```bash
docker compose exec db psql -U appuser -d appdb -c "SELECT id, COUNT(*) FROM pets GROUP BY id HAVING COUNT(*) > 1;"
```

No rows returned means no duplicate records.

## Project Files

- `main.py` - application flow
- `api.py` - Swagger Petstore API call
- `databese.py` - PostgreSQL connection and insert logic
- `docker-compose.yml` - app, database, network, healthcheck, and volume setup
- `Dockerfile` - image definition used for publishing the app image
