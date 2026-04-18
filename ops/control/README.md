# control — deploy / stop buttons

Local-only web UI with two buttons that run `docker compose` in a target directory.
**Do not expose this to the internet without auth** — it executes shell commands.

## Run (dev, no container)

```bash
cd ops/control
pip install -r requirements.txt
COMPOSE_DIR=/path/to/OpenMetadata uvicorn app:app --host 127.0.0.1 --port 8080
```

Open http://127.0.0.1:8080

## Run (containerised)

```bash
docker build -t opendataworld-control ops/control
docker run --rm \
  -p 127.0.0.1:8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/OpenMetadata:/app/target \
  -e COMPOSE_DIR=/app/target \
  opendataworld-control
```

## Config

| Env var | Default | Purpose |
|---|---|---|
| `COMPOSE_DIR` | `/app/target` | Directory containing `docker-compose.yml` |
| `COMPOSE_PROFILES` | *(empty)* | Comma-separated profiles to activate |

## Endpoints

| Method | Path | Runs |
|---|---|---|
| GET | `/` | Serves the HTML UI |
| POST | `/deploy` | `docker compose up -d --pull always` |
| POST | `/stop` | `docker compose down` |
| GET | `/status` | `docker compose ps --format json` |

## Security

- Binds to `127.0.0.1` only. Access from outside the host requires SSH tunnel.
- Mounting the Docker socket gives the container root-equivalent access to the host — only run on machines you fully control.
- For exposure to real users, put **oauth2-proxy + Keycloak** in front and flip the bind to `0.0.0.0`.
