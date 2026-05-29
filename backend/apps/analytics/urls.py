from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerformanceSnapshotViewSet
router = DefaultRouter()
router.register(r'performance', PerformanceSnapshotViewSet)
urlpatterns = [path('', include(router.urls))]
