from django.contrib import admin
from .models import *
from collection.admin import MuseumCollectionInline


class MuseumUserInline(admin.TabularInline):
    model = MuseumUser
    fields = ("user", "museum", "position", "joined_at")

    readonly_fields = ("id", "joined_at", "user")
    can_delete = True
    max_num = 0
    extra = 0
    show_change_link = True


class MuseumAdmin(admin.ModelAdmin):
    list_display = ("id", "short_name", "name", "created_at", "updated_at")
    list_display_links = ("id", "name", "short_name")
    search_fields = ("id", "name", "address", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("id", "created_at", "updated_at")
    save_on_top = True
    inlines = (MuseumUserInline, MuseumCollectionInline)


class MuseumUserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "museum", "position")
    list_display_links = ("id", "user")
    search_fields = ("id", "user", "museum", "joined_at")
    list_filter = ("museum", "joined_at")
    readonly_fields = ("id", "joined_at")
    save_on_top = True


admin.site.register(Museum, MuseumAdmin)
admin.site.register(MuseumUser, MuseumUserAdmin)
