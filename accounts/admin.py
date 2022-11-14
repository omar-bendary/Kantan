from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import OTP, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone_number', 'is_verified']
    fieldsets = (
        (None, {'fields': ('phone_number', 'is_verified',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', ),
        }),
    )
    ordering = ('phone_number',)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_expired', 'user',
                    'created_at', 'reset_password_permission']
    fieldsets = (
        (None, {'fields': ('code', 'is_expired')}),
    )
    ordering = ('created_at',)
