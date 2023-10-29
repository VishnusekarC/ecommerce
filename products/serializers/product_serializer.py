from rest_framework import serializers
from products.models import Product


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('ppoi', 'is_active', 'categories', 'collections', 'created_at', 'updated_at')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request:
            if obj.image:
                return request.build_absolute_uri(obj.image.url)
        return None