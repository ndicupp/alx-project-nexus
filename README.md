# Nexus ProDev E-Commerce Backend

## Project Overview
This repository contains the backend system for a scalable, high-performance E-Commerce platform. Built as the capstone project for the **ALX ProDev Backend Engineering** program, this system demonstrates advanced backend methodologies, including professional database design, secure authentication, and containerized deployment.

### Key Goals
- **Scalability:** Optimized PostgreSQL schema for large product catalogs.
- **Security:** Bulletproof authentication using JWT (JSON Web Tokens).
- **Documentation:** Interactive API reference using Swagger/OpenAPI.
- **Performance:** Efficient querying with indexing and pagination.

---
## Challenges & Solutions

| Challenge | Solution |
| :--- | :--- |
| **Environment Mismatch** | Implemented **Docker** to containerize the Django app and PostgreSQL database, ensuring "it works on my machine" translates to everyone's machine. |
| **Slow API Responses** | Offloaded time-consuming tasks (like email notifications) to **Celery workers** to keep the main request-response cycle fast. |
| **Documentation Clarity** | Integrated **Swagger/OpenAPI** to provide interactive documentation for frontend collaborators. |

## Best Practices & Takeaways
- **Test-Driven Development:** Writing unit and integration tests early to catch bugs before they reach production.
- **Clean Code:** Adhering to PEP 8 standards and modular design for maintainability.
- **Collaboration is Key:** Engaging with Frontend learners early in the lifecycle to define clear API contracts.

## Tech Stack
- **Framework:** Django 5.0 + Django REST Framework (DRF)
- **Database:** PostgreSQL (Relational)
- **Security:** SimpleJWT (Authentication)
- **DevOps:** Docker & Docker Compose
- **API Docs:** drf-spectacular (Swagger UI)

---

## Getting Started (Docker)
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/alx-project-nexus.git
   cd alx-project-nexus

## Project Status / Roadmap
## ecommerce-backend/
├── docker/
│   └── entrypoint.sh
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── users/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── apps.py
│   └── manage.py
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

### Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "/app/docker/entrypoint.sh"]

#### docker-compose.yml
version: "3.9"

services:
  backend:
    build: .
    container_name: ecommerce_backend
    command: python src/manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:16
    container_name: ecommerce_db
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: ecommerce_user
      POSTGRES_PASSWORD: ecommerce_password
    volumes:
      - postgres_data:/var/lib/postgresql/data/

volumes:
  postgres_data:

##### docker/entrypoint.sh
#!/bin/sh

python src/manage.py migrate --noinput
python src/manage.py collectstatic --noinput || true

exec "$@"

Make it executable:
chmod +x docker/entrypoint.sh

##### requirements.txt
Django>=5.0
djangorestframework
psycopg2-binary
python-dotenv
djangorestframework-simplejwt
drf-spectacular

##### Django Project Initialization
run once (outside Docker):
docker-compose run backend django-admin startproject core src

Then create the users app:
docker-compose run backend python src/manage.py startapp users

##### users/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

##### users/admin.py
from django.contrib import admin
from .models import User

admin.site.register(User)

##### core/settings.py
Add apps:
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "drf_spectacular",

    "users",
]

Custom user model:
AUTH_USER_MODEL = "users.User"

PostgreSQL config:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecommerce",
        "USER": "ecommerce_user",
        "PASSWORD": "ecommerce_password",
        "HOST": "db",
        "PORT": 5432,
    }
}

##### JWT + Swagger Setup
REST Framework:
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

Swagger:
SPECTACULAR_SETTINGS = {
    "TITLE": "E-Commerce API",
    "DESCRIPTION": "Project Nexus – ProDev Backend",
    "VERSION": "1.0.0",
}

##### core/urls.py
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]

##### Run the System
docker-compose up --build
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py migrate

Then:

Admin: http://localhost:8000/admin/

Swagger: http://localhost:8000/api/docs/

## Collaboration Hub
This project is designed with collaboration at its core. 
- **Frontend Integration:** API endpoints are documented via Swagger for seamless integration.
- **Discord:** Active participant in the `#ProDevProjectNexus` channel.

---
*Created as part of the ProDev Backend Engineering Program - 2026.*
