from rest_framework import serializers
from accounts.models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_email(self, value):
        users = CustomUser.objects.filter(email=value)
        if not users.exists():
            raise serializers.ValidationError("Must register to login")

        if not users.first().is_active:
            raise serializers.ValidationError("Please activate your account, and login")
                
        return value