from django.urls import path
from .views import ExchangeListView

urlpatterns = [
    path('', ExchangeListView.as_view(), name='exchange-list'),
]
