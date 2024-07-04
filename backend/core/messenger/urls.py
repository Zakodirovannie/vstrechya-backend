from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import ConversationViewSet, MessageViewSet
from django_channels_jwt.views import AsgiValidateTokenView

router = SimpleRouter()

router.register("conversations", ConversationViewSet)
router.register("messages", MessageViewSet)

app_name = "messanger"
urlpatterns = router.urls
urlpatterns += [path("auth/wslogin", AsgiValidateTokenView.as_view())]
