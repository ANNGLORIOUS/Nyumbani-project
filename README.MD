# Nyumbani Project

Nyumbani is a Django-based property management system for:

- user registration and login
- property listing and management
- maintenance request tracking
- rent payment tracking
- optional SMS notifications
- optional M-Pesa integration

This project is set up so it can run locally even if you do not have live SMS or M-Pesa credentials yet.

## What is already working

- the project starts correctly
- the main API routes are connected
- property endpoints now return API responses instead of a missing HTML page
- M-Pesa can run in safe simulation mode for demos and testing
- SMS sending is disabled by default so local use does not fail
- automated smoke tests pass

## Before you start

You need:

- Python 3.8 or newer
- internet access only for the first dependency install
- a terminal

## Simple setup guide

Follow these steps in order.

1. Open the project folder in your terminal.

2. Install the required packages:

```bash
python3 -m pip install -r requirements.txt
```

3. Create your environment file:

```bash
cp .env.example .env
```

4. Apply database migrations:

```bash
python3 manage.py migrate
```

5. Start the project:

```bash
python3 manage.py runserver
```

6. Open this address in your browser:

```text
http://127.0.0.1:8000/
```

If the project is running well, you will see a small JSON response showing the system status and the main API routes.

## Main links

- Home: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`
- Users API: `http://127.0.0.1:8000/api/users/`
- Properties API: `http://127.0.0.1:8000/api/properties/`
- Payments API: `http://127.0.0.1:8000/api/payments/`

## If you want an admin account

Run this command:

```bash
python3 manage.py createsuperuser
```

Then sign in at:

```text
http://127.0.0.1:8000/admin/
```

<!-- ## Important note about payments

This project is currently set to:

- `MPESA_SIMULATE=true`

That means payments can be tested without connecting to a real M-Pesa account. This is the best option for demos, school work, local testing, and non-technical users.

If you want to use real M-Pesa later, add real values into `.env` and change:

```text
MPESA_SIMULATE=false
``` -->

## Important note about SMS

This project is currently set to:

- `SMS_ENABLED=false`

That means the app will skip sending real SMS messages unless you explicitly enable it.

If you want real SMS sending later:

1. Add your Africa's Talking credentials to `.env`
2. Change `SMS_ENABLED=false` to `SMS_ENABLED=true`

## Basic usage flow

For a simple demo, use this order:

1. Register users through the users API.
2. Log in and get a token.
3. Create a property as an owner.
4. Create maintenance requests as a tenant.
5. Initiate a payment as a tenant.
6. View payment history.

## API endpoints

### Users

- Register: `POST /api/users/register/`
- Login token: `POST /api/token/`
- Refresh token: `POST /api/token/refresh/`
- Maintenance list/create: `GET or POST /api/users/maintenance/`

### Properties

- List properties: `GET /api/properties/`
- Create property: `POST /api/properties/`
- View one property: `GET /api/properties/<id>/`
- Update property: `PUT /api/properties/<id>/`

### Payments

- Start payment: `POST /api/payments/mpesa/pay/`
- Payment callback: `POST /api/payments/mpesa/callback/`
- Payment history: `GET /api/payments/history/`

## How to send authenticated requests

Some endpoints require login.

1. First get an access token from:

```text
POST /api/token/
```

2. Then include it in your request header like this:

```text
Authorization: Bearer your_access_token
```

## Common problems and easy fixes

### The server does not start

Run:

```bash
python3 -m pip install -r requirements.txt
python3 manage.py migrate
```
<!-- 
### Payments are not reaching real M-Pesa

Check your `.env` file. If `MPESA_SIMULATE=true`, the project is intentionally using demo mode.

### SMS is not being sent

That is expected unless `SMS_ENABLED=true` and valid Africa's Talking credentials are provided.

### I want to confirm the project is healthy

Run:

```bash
python3 manage.py check
python3 manage.py test users.tests properties.tests payments.tests
``` -->
<!-- 
## For a developer or technical helper

Verified locally with:

```bash
python3 manage.py check
python3 manage.py test users.tests properties.tests payments.tests
``` -->

<!-- ## Summary

The project is ready for local use, demo use, and further improvement. It now starts correctly, has safer local behavior, and includes instructions that a non-technical person can follow step by step. -->
