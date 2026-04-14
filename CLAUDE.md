# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Python scripts to manage a TrueNAS SCALE server (v25.10.2.1) via its REST API, accessed over Tailscale.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install requests python-dotenv
```

Create a `.env` file (never commit this):
```
TRUENAS_HOST=100.86.174.15
TRUENAS_PORT=20443
TRUENAS_HOSTNAME=truenas
TRUENAS_API_KEY=<api-key>
TRUENAS_USER=admin
TRUENAS_PASSWORD=<password>
```

## Running

```bash
.venv/bin/python client.py   # test connection / system info
```

## Architecture

- `client.py` — shared `session` (requests.Session with API key auth), `get()`/`post()` helpers, and `login(user, password)` for Basic auth sessions. Import this in other scripts.
- `.env` — credentials (gitignored)

## Connectivity

| Method | Address |
|--------|---------|
| API    | `https://100.86.174.15:20443/api/v2.0` |
| Web UI | `http://100.86.174.15:20080` |
| SSH    | `ssh admin@100.86.174.15` (key auth) |

API docs: http://100.86.174.15:20080/api/docs  
Self-signed cert — `session.verify = False` is intentional.

## API auth

Two methods both work:
1. **API key** — `Authorization: Bearer <key>` header (default `session` in client.py)
2. **Basic auth** — `login(username, password)` returns a requests.Session
