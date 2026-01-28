#ecommerce-backend

ecommerce-backend/
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

#Dockerfile

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

#docker-compose.yml

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


#docker/entrypoint.sh

#!/bin/sh

python src/manage.py migrate --noinput
python src/manage.py collectstatic --noinput || true

exec "$@"

chmod +x docker/entrypoint.sh

#requirements.txt

Django>=5.0
djangorestframework
psycopg2-binary
python-dotenv
djangorestframework-simplejwt
drf-spectacular

docker-compose run backend django-admin startproject core src

docker-compose run backend python src/manage.py startapp users

#users/models.py

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

#users/admin.py

from django.contrib import admin
from .models import User

admin.site.register(User)

#core/settings.py
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

AUTH_USER_MODEL = "users.User"

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


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "E-Commerce API",
    "DESCRIPTION": "Project Nexus – ProDev Backend",
    "VERSION": "1.0.0",
}

#core/urls.py
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]

docker-compose up --build

docker-compose run backend python src/manage.py makemigrations
docker-compose run backend python src/manage.py migrate
docker-compose run backend python src/manage.py createsuperuser

POST /api/auth/register/
{
  "email": "user@test.com",
  "password": "TestPass123"
}

POST /api/auth/login/
{
  "email": "user@test.com",
  "password": "TestPass123"
}

git add .
git commit -m "feat: implement custom user model and JWT authentication"
git push



