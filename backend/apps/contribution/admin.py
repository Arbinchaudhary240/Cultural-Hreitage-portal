from django.contrib import admin
from .models import Contribution
from django.utils.safestring import mark_safe

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ['title', 'contributer', 'status', 'added_at', 'has_media']
    list_filter = ['status', 'added_at']
    search_fields = ['title', 'description', 'contributer__email', 'contributer__username']
    actions = ['approve_contributions', 'reject_contributions']

    def has_media(self, obj):
        """Quickly see if the contribution has files attached"""
        return bool(obj.image or obj.audio or obj.video)
    has_media.boolean = True
    has_media.short_description = 'Media?'

    def approve_contributions(self, request, queryset):
        queryset.update(status='approved')
    approve_contributions.short_description = "Mark selected as Approved"

    def reject_contributions(self, request, queryset):
        queryset.update(status='rejected')
    reject_contributions.short_description = "Mark selected as Rejected"

    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "No Image"