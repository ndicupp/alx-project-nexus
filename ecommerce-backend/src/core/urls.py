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
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py migrate

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]


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

docker-compose run backend python src/manage.py startapp categories
docker-compose run backend python src/manage.py startapp products

path("api/categories/", include("categories.urls")),
path("api/products/", include("products.urls")),


from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

urlpatterns = [
    # ... your other URLs (admin, apps)
    
    # 1. The Schema (YAML/JSON raw file)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Swagger UI (Interactive & Colorful)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Redoc (Clean & Minimalist alternative)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


import debug_toolbar

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
] + urlpatterns
