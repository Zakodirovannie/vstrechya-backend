from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Museum, MuseumUser
from .serializers import MuseumSerializer
from core.utils import delete_cache


class MuseumViewSet(APIView):
    """
    ViewSet museums

    * Sometimes requires authentication.
    """

    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer
    CACHE_KEY_PREFIX = "museum-view"

    @method_decorator(cache_page(300, key_prefix=CACHE_KEY_PREFIX))
    def get(self, request: Request, *args, **kwargs):
        """
        Get museum by id.
        """
        museum = self.queryset.get(pk=kwargs["id"])
        serializer = self.serializer_class(museum)
        return Response(serializer.data)

    def patch(self, request: Request, *args, **kwargs):
        """
        Patch museum by id.
        """
        try:
            museum_user = MuseumUser.objects.get(
                user_id=request.user.id, museum_id=kwargs["id"]
            )
            if museum_user and museum_user.access_level >= 3:
                museum = self.queryset.get(pk=kwargs["id"])
                serializer = self.serializer_class(museum, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    delete_cache(self.CACHE_KEY_PREFIX)
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"status": "failed", "error": e.args}, status=status.HTTP_403_FORBIDDEN
            )


class MuseumList(APIView):
    """
    View to list all museums in the system.
    """

    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer
    CACHE_KEY_PREFIX = "museum-view"

    @method_decorator(cache_page(300, key_prefix=CACHE_KEY_PREFIX))
    def get(self, request: Request, *args, **kwargs):
        """
        Return a list of all users.
        """
        serializer = self.serializer_class(Museum.objects.all(), many=True)
        return Response(serializer.data)
