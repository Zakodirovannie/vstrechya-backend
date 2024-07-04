from django.contrib import admin
from .models import *

# Register your models here.


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "created_at", "email", "phone")
    list_display_links = ("id", "email")
    search_fields = ("id", "email", "first_name", "last_name")
    readonly_fields = ("id", "created_at", "password", "last_login")


admin.site.register(UserAccount, UserAccountAdmin)
