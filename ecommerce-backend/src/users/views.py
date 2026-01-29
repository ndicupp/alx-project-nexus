from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] # Open to everyone

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "email": user.email,
                    "id": user.id
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# We use the built-in SimpleJWT Login View
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


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
