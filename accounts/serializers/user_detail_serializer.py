from rest_framework import serializers
from accounts.models import CustomUserDetail


class CreateCustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserDetail
        fields = ('username', 'mobile_number', 'avatar')

    def create(self, user, validated_data):
        user_detail = CustomUserDetail.objects.create(
            user=user,
            **validated_data
        )
        return user_detail

class GenericCustomUserDetailSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUserDetail
        fields = ('username', 'mobile_number', 'avatar_url')

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if request:
            if obj.avatar:
                return request.build_absolute_uri(obj.avatar.url)
        return None
            
