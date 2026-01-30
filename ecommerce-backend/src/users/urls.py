from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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

import debug_toolbar

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
] + urlpatterns

git add .
git commit -m "perf: add database indexes and optimize product queries"
git push

