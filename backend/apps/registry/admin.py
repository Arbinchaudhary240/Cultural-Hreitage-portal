from django.contrib import admin
from .models import Category, HeritageItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Automatically types the slug as you type the name

@admin.register(HeritageItem)
class HeritageItemAdmin(admin.ModelAdmin):
    list_display = ('official_name', 'category', 'get_contributor')
    list_filter = ('category',)
    search_fields = ('official_name', 'contribution__description')
    
    fieldsets = (
        ("Basic Info", {
            'fields': ('official_name', 'category', 'desciption')
        }),
        ("The Link", {
            'description': "Link this to an APPROVED contribution from a user.",
            'fields': ('contribution',)
        }),
        ("Extra Details", {
            'fields': ('metadata',),
        }),
    )

    def get_contributor(self, obj):
        # Shows the username of the person who made the contribution in the list view
        return obj.contribution.contributer.username
    get_contributor.short_description = 'Submitted By'