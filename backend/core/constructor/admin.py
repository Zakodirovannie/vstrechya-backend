from django.contrib import admin
from .models import ConstructedCollection, UserConstructedCollection

admin.site.register(ConstructedCollection)
admin.site.register(UserConstructedCollection)
