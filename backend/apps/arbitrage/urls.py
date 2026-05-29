from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArbitrageOpportunityViewSet

router = DefaultRouter()
router.register(r'', ArbitrageOpportunityViewSet, basename='arbitrageopportunity')

urlpatterns = [
    path('', include(router.urls)),
]
