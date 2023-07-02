from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User


# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ["id", "email", "is_staff", "is_active", "is_superuser"]
    list_filter = ["id", "email", "is_staff", "is_active", "is_superuser"]
    list_per_page = 10
    ordering = ["id", "email"]
    readonly_fields = ["id", "last_login"]
    search_fields = ["id", "email"]

    fieldsets = [
        (
            None,
            {
                "fields": ["id", "email", "password"],
            },
        ),
        (
            "Permissions",
            {
                "fields": ["is_active", "is_staff", "is_superuser"]
            }
        ),
        (
            None,
            {
                "fields": ["last_login"]
            }
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ],
            },
        ),
    ]


admin.site.register(User, UserAdmin)
