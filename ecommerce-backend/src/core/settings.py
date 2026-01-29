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

AUTH_USER_MODEL = "users.User"

from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

docker-compose run backend python src/manage.py startapp categories
docker-compose run backend python src/manage.py startapp products

pip install django-filter

INSTALLED_APPS += ["django_filters"]
