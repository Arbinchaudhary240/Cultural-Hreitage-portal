from rest_framework import serializers
from .models import EthnicityProfile

class SubNodeSerializer(serializers.ModelSerializer):
    """Simplified nesting serializer to map downward relationships."""
    class Meta:
        model = EthnicityProfile
        fields = ['id', 'name', 'slug', 'node_type']

class EthnicityProfileSerializer(serializers.ModelSerializer):
    # This automatically nests child nodes (Religion -> Castes -> Subcastes)
    children = SubNodeSerializer(many=True, read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = EthnicityProfile
        fields = ['id', 'name', 'slug', 'node_type', 'parent', 'parent_name', 'children', 'historical_background']