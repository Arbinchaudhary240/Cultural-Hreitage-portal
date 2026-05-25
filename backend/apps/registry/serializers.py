from rest_framework import serializers
from .models import Category,HeritageItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'name']
        
class HeritageItemSerializer(serializers.ModelSerializer):
    contributor_description = serializers.CharField(source='contribution.description', read_only=True)
    video = serializers.FileField(source='contribution.video', read_only=True)
    audio = serializers.FileField(source='contribution.audio', read_only=True)
    image = serializers.ImageField(source='contribution.image', read_only=True)
    shared_by = serializers.CharField(source='contribution.contributer.username', read_only=True)

    class Meta:
        model = HeritageItem
        fields = [
            'id', 
            'official_name',
            'category', 
            'contributor_description', # Their full story/details
            'video', 
            'audio', 
            'image',
            'shared_by',
            'metadata' # Keeping this for any extra 'Tags' you might add later
        ]

