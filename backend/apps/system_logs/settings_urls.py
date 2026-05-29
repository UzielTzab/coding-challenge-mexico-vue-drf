from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BotRuntimeStateViewSet

router = DefaultRouter()
router.register(r'', BotRuntimeStateViewSet, basename='botruntimestate')

urlpatterns = [
    path('', include(router.urls)),
]
