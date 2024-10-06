from rest_framework import serializers, ISO_8601

from core.category.application.dto import CategoryOutput

class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)
    