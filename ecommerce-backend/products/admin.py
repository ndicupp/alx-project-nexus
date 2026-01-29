from django.contrib import admin
from .models import Product

admin.site.register(Product)


docker-compose run backend python src/manage.py makemigrations
docker-compose run backend python src/manage.py migrate
