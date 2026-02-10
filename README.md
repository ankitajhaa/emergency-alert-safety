# Emergency Alert & Safety Broadcast API

Backend system for managing emergency alerts and safety broadcasts within a campus or organization. Administrators can create and manage alerts, while users can view active alerts and acknowledge that they have seen them.
 
---

## Tech Stack

- Python / Django
- Django REST Framework
- JWT Authentication
- PostgreSQL
- Docker & Docker Compose

---

## Features

### Authentication & Roles
- User registration
- JWT login
- Role based access (`ADMIN`, `USER`)

### Alert Management
- Admins can create alerts
- Admins can update or resolve alerts
- All alerts stored with creator and timestamp

### User Feed
- Admin → see all alerts
- Normal users → see only ACTIVE alerts

### Acknowledgement System
- Users can acknowledge an alert
- Duplicate acknowledgements are blocked
- Timestamp recorded

### Business Rules
- Only admins can modify alerts
- Resolved alerts remain for history/audit
- One acknowledgement per user per alert

----

## Setup

docker compose build
docker compose up

----

## Authentication

Create user:
POST /users/create/

Login:
POST /users/token/

Use header:
Authorization: Bearer <access_token>

----

## Endpoints

Alerts:
GET /alerts/
GET /alerts/active/
POST /alerts/ (admin only)
POST /alerts/{id}/ack/ (user only)

----

## Running Tests

docker compose run --rm app python manage.py test