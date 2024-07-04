from django.urls import path

from .views import MuseumViewSet, MuseumList

urlpatterns = [
    path("museums/", MuseumList.as_view(), name="museum"),
    path("museum/<int:id>", MuseumViewSet.as_view(), name="museum"),
]
