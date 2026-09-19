# Nyumbani backend

This directory contains the Django REST API for Nyumbani. The React application
lives in `../frontend/`.

## Run locally

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 manage.py migrate
python3 manage.py seed_demo_data
python3 manage.py runserver
```

The API starts at `http://127.0.0.1:8000/`; the React application proxies its
`/api` requests here during development.

## Demo accounts

| Role | Username | Password |
| --- | --- | --- |
| Landlord | `landlord_demo` | `DemoPass123` |
| Agent | `agent_demo` | `DemoPass123` |
| Tenant | `tenant_demo` | `DemoPass123` |

These accounts are created by `seed_demo_data` and are for local demos only.
