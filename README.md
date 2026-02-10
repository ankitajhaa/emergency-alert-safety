# Emergency Alert & Safety Broadcast

## Objective: A Backend API for managing emergency alerts and safety broadcasts within a campus or organization. The system should allow administrators to create alerts and users to receive, acknowledge, and track critical safety information.

----

## Tech Stack
- Django
- Django REST Framework
- JWT Authentication
- PostgreSQL
- Docker

----

## Features:
- User registration and login
- Token-based authentication
- Support for Admin and Normal User roles

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