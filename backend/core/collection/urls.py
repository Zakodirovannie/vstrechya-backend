from django.urls import path
from .views import CollectionsViewSet, CollectionsItemViewSet

urlpatterns = [
    path(
        "collections/<int:collection_id>/",
        CollectionsViewSet.as_view({"get": "get_collection_by_id"}),
        name="collections",
    ),
    path(
        "collections/create/",
        CollectionsViewSet.as_view(
            {"get": "collection_create_get", "post": "collection_create_post"}
        ),
        name="collections",
    ),
    path(
        "collections/<int:collection_id>/items/add/",
        CollectionsItemViewSet.as_view(
            {"get": "collection_item_create_get", "post": "collection_item_create_post"}
        ),
        name="collections",
    ),
]
