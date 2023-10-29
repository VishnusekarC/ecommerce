from rest_framework import serializers
from accounts.models import CustomUser

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_email(self, value):
        users = CustomUser.objects.filter(email=value)
        if users.exists():
            if users.first().is_active:
                raise serializers.ValidationError("Email address is already in use")
            else:
                raise serializers.ValidationError("Please activate your account")
        return value

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if len(password) < 8:
            raise serializers.ValidationError("Passwords must be 8 characters or more")


        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return data
        
        

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = CustomUser.objects.create_user(email=email, password=password)
        return user