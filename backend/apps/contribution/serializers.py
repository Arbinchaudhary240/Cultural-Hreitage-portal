from rest_framework import serializers
from .models import Contribution

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["id", "title", "description", "image", "audio", "vedio", "added_at"]
        read_only_fields = ["id", "added_at"]