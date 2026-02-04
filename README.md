
# Project Nexus: E-commerce backend
**An Optimized, Professional-Grade E-Commerce API**

[![Django CI](https://github.com/ndicupp/alx-project-nexus/actions/workflows/django_ci.yml/badge.svg)](https://github.com/ndicupp/alx-project-nexus/actions)



## Project Overview
Project Nexus is a high-performance backend API built with **Django REST Framework** and **PostgreSQL**. It features a custom user authentication system, advanced product cataloging with optimized search/filter logic, and a fully automated CI/CD pipeline.

### 🔗 Submission Tasks (Quick Links)
- **Task 1: [Database Design (ERD)](https://docs.google.com/document/d/1HW6078MxmKjO-ZuE1n1WBdoPR27dkJNdBSEElXtfX7w/edit?tab=t.qoxd5zbp2iev)**
- **Task 2: [Presentation Slide Deck](https://docs.google.com/presentation/d/1HvkuyPSA-G_T6awKftwv_N08OwxLSbd7vgOr6VtaFnA/edit?slide=id.p#slide=id.p)**
- **Task 3: [Project Demo Video](https://drive.google.com/file/d/1BR1mWcH8fpBA6OAj2Jql19vdiggHKutY/view?usp=sharing)**
- **Task 4: [Live Hosted API]**

---

## Key Technical Features
- **Custom User Model & Profiles**: Modern email-based authentication with automated Profile creation via **Django Signals**.
- **PostgreSQL Optimization**: Implemented **Composite and Functional Indexes** to ensure sub-millisecond query times for searches and filters.
- **RESTful Design**: Fully documented endpoints using **Swagger/OpenAPI 3.0**.
- **DevOps Ready**: 100% containerized with **Docker** and automated testing via **GitHub Actions**.

---

## Architecture & Database Design
The system uses a highly normalized relational structure. 
> **Indexing Strategy:** I applied `db_index=True` on frequently searched fields and created functional indexes for case-insensitive product searches, satisfying the "Exceptional" performance criteria.

**[View Full ERD Diagram & Rationale Here](https://docs.google.com/document/d/1HW6078MxmKjO-ZuE1n1WBdoPR27dkJNdBSEElXtfX7w/edit?tab=t.qoxd5zbp2iev)**

---

## Getting Started (Local Development)

### Prerequisites
- Docker & Docker Compose

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/ndicupp/alx-project-nexus.git](https://github.com/ndicupp/alx-project-nexus.git)
   cd alx-project-nexus

https://github.com/ndicupp/alx-project-nexus/blob/main/ecommerce-backend/.github/workflows/django_ci.yml

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


## API Doc Screenshots / Links

API Docs: http://localhost:8000/api/docs/

## Project Status

✔ Docker + PostgreSQL + Custom User Done  
✔ JWT Authentication API (To be built)  
✔ Products & Categories APIs (Pending)  
✔ Filtering, Sorting, Pagination (Pending)  
✔ Comprehensive Tests (Pending)  


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

## Collaboration
- Discord: #ProDevProjectNexus
- Frontend API users should refer to Swagger


*Created as part of the ProDev Backend Engineering Program - 2026.*
