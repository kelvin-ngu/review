from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .rooms import ModerationRoomView #AddModeratorView

# router = DefaultRouter()
# router.register('rooms', ModerationRoomViewSet, basename='room')

urlpatterns = [
    # path('', include(router.urls)),
    path('rooms/', ModerationRoomView.as_view())
]