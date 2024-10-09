from rest_framework import serializers, ISO_8601

from core.__seedwork.application.dto import PaginationOutput
from core.__seedwork.infra.django_app.serializers import CollectionSerializer, PaginationSerializer

class CategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)
    
    
class CategoryCollectionSerializer(CollectionSerializer):
    child = CategorySerializer()
