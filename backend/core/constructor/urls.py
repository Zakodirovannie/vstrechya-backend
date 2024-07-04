from django.urls import path
from .views import ConstructedCollectionViewSet

urlpatterns = [
    path(
        "constructor/collections/<int:pk>/",
        ConstructedCollectionViewSet.as_view({"get": "get_collection_by_id"}),
        name="constructed-collections",
    ),
    path(
        "constructor/collections/create/",
        ConstructedCollectionViewSet.as_view(
            {"get": "create_collection_get", "post": "create_collection_post"}
        ),
        name="constructed-collections-create",
    ),
    path(
        "constructor/collections/<int:pk>/upload-json/",
        ConstructedCollectionViewSet.as_view({"post": "upload_json_data"}),
        name="upload-json-data",
    ),
]
