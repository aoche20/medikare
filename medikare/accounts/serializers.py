from rest_framework import serializers
from accounts.models import User
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'full_name', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
