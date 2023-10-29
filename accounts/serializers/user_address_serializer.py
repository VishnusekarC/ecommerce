from rest_framework import serializers
from accounts.models import CustomUserAddress, CustomUser

class CreateUserAddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = CustomUserAddress
        fields = '__all__'

    def save(self, user, **kwargs):
        validated_data = self.validated_data
        custom_user_address = CustomUserAddress.objects.create(user=user, **validated_data)
        return custom_user_address


class UserAddressSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = CustomUserAddress
        exclude = ('created_at', 'updated_at', 'user', 'state', 'city')
