from django.contrib import admin
from .models import EthnicityProfile

@admin.register(EthnicityProfile)
class EthnicityProfileAdmin(admin.ModelAdmin):
    # Dynamic list layout
    list_display = ('name', 'node_type', 'get_parent_link', 'slug')
    list_filter = ('node_type',)
    search_fields = ('name', 'historical_background')
    prepopulated_fields = {'slug': ('name',)}
    
    # Clean form segmentation
    fieldsets = (
        ("Core Identity", {
            'fields': ('name', 'slug', 'node_type')
        }),
        ("Hierarchical Relationship", {
            'description': "Connect this node to its broader parent category (e.g., Subcaste -> Caste -> Religion).",
            'fields': ('parent',),
        }),
        ("Contextual Records", {
            'fields': ('historical_background',),
        }),
    )

    def get_parent_link(self, obj):
        """Displays the parent node with its assignment type clarity."""
        if obj.parent:
            return f"{obj.parent.name} [{obj.parent.get_node_type_display()}]"
        return "Root Node"
    get_parent_link.short_description = 'Parent Node'