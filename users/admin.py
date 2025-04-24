from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'firstName', 'lastName', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'firstName', 'lastName')
    fieldsets = (
        (None, {'fields': ('email', 'firstName', 'lastName', 'zipCode', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstName', 'lastName', 'zipCode', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(User, CustomUserAdmin)