# Nyumbani — Property Management & Rental Operations

Nyumbani is a Django REST platform for property listings, tenant operations,
rent obligations, M-Pesa payment reconciliation, and SMS notifications.

## What is available

- Public property browsing: `GET /api/properties/`
- Owner, agent, tenant, and administrator roles (legacy caretaker accounts remain supported)
- Rich listings: location, bedrooms, bathrooms, amenities, availability, and images
- Inquiries and maintenance requests
- Leases and monthly `RentRecord` obligations, including due dates, balances, and status
- M-Pesa payment records linked to rent records and reconciled on callback
- Durable notifications with optional asynchronous Celery/Africa's Talking delivery

## Project structure

```text
Nyumbani-project/
├── backend/       Django REST API, migrations, environment settings, and database
├── frontend/      React, TypeScript, Tailwind, and Vite application
└── README.MD
```

## Demo login details

After running the backend seed command, use these accounts in the React login
screen:

| Role | Username | Password |
| --- | --- | --- |
| Property owner / landlord | `landlord_demo` | `DemoPass123` |
| Agent / caretaker | `agent_demo` | `DemoPass123` |
| Tenant | `tenant_demo` | `DemoPass123` |

These are local demo accounts only. Change their passwords or remove them
before deploying the application.

## Local setup

```bash
cd backend
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 manage.py migrate
python3 manage.py seed_demo_data
python3 manage.py runserver
```

In a second terminal, start the React frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173/`. Vite proxies `/api` requests to the Django
server at port 8000. The Django root URL is now an API status response, not a
second competing interface.

Run backend checks from the `backend/` directory:

```bash
python3 manage.py check
python3 manage.py test users.tests properties.tests payments.tests notifications.tests
```

## Core endpoints

- `POST /api/users/register/`
- `GET /api/users/me/` (the current authenticated user)
- `POST /api/token/`
- `GET, POST /api/properties/` (GET is public; POST requires an owner or agent)
- `GET, PUT, DELETE /api/properties/<id>/`
- `GET, POST /api/properties/<id>/inquiries/`
- `GET, POST /api/users/maintenance/`
- `POST /api/payments/mpesa/pay/`
- `POST /api/payments/mpesa/callback/`
- `GET /api/payments/history/`

Pass `rent_record` when initiating a payment to connect it to the tenant's rent
obligation. A confirmed callback updates `amount_paid`, the balance, and the
rent-record status atomically.

## Notifications

Application code uses `notifications.services.notify()`; it never sends SMS
from a view or on import. SMS delivery is queued with Celery only when both a
broker and `NOTIFICATIONS_ASYNC=true` are configured. Keep `SMS_ENABLED=false`
for local development. Production secrets belong in `.env`, never version
control.
