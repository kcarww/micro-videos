from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)