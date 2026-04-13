from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'full_name', 'is_staff', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('full_name', 'phone', 'country', 'city', 'profile')}),
    )

admin.site.register(User, CustomUserAdmin)