from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemLogViewSet, BotRuntimeStateViewSet

router = DefaultRouter()
router.register(r'', SystemLogViewSet, basename='systemlog')
router.register(r'settings', BotRuntimeStateViewSet, basename='botruntimestate')

urlpatterns = [
    path('', include(router.urls)),
]
