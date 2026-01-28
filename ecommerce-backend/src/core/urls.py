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


