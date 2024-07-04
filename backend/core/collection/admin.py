from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.


class MuseumCollectionInline(admin.TabularInline):
    model = MuseumCollection
    fields = ("collection", "created_at")

    readonly_fields = ("id", "created_at", "collection", "museum")
    can_delete = True
    max_num = 0
    extra = 0
    show_change_link = True


class MuseumCollectionAdmin(admin.ModelAdmin):
    list_display = ("id", "collection", "museum", "created_at")
    list_display_links = (
        "id",
        "collection",
    )
    list_filter = ("museum",)
    search_fields = ("id", "museum")
    readonly_fields = ("id", "created_at", "updated_at")


class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    fields = ("get_photo", "created_at", "updated_at")

    readonly_fields = ("id", "created_at", "updated_at", "get_photo")
    can_delete = True
    max_num = 0
    extra = 0
    show_change_link = True

    def get_photo(self, object):
        return (
            mark_safe(f'<img src="{object.image_url}" width=150>')
            if object.image_url
            else "-"
        )

    get_photo.short_description = "Превью"


class CollectionAdmin(admin.ModelAdmin):
    fields = ("name", "id", "created_at")
    readonly_fields = ("id", "created_at")
    inlines = [CollectionItemInline]


class CollectionItemAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "collection",
        "image_url",
        "description",
        "get_photo",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("id", "get_photo", "created_at", "updated_at")

    def get_photo(self, object):
        return (
            mark_safe(f'<img src="{object.image_url}" width=400>')
            if object.image_url
            else "-"
        )

    get_photo.short_description = "Превью"


class UserCollectionAdmin(admin.ModelAdmin):
    fields = ("user", "collection", "id")
    readonly_fields = ("user", "collection", "id")


admin.site.register(Collection, CollectionAdmin)
admin.site.register(UserCollection, UserCollectionAdmin)
admin.site.register(CollectionItem, CollectionItemAdmin)
admin.site.register(MuseumCollection, MuseumCollectionAdmin)
