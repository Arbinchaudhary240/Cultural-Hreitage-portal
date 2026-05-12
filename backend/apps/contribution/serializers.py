from rest_framework import serializers
from .models import Contribution

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["id", "title", "description", "image", "audio", "video", "added_at"]
        read_only_fields = ["status","id", "added_at"]