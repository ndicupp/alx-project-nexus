from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        # Using the manager's create_user ensures password hashing
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

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
