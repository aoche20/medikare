from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from accounts.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
