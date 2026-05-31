from django.urls import path
from .views import WalletListView, WalletMovementListView

urlpatterns = [
    path('', WalletListView.as_view(), name='wallet-list'),
    path('movements/', WalletMovementListView.as_view(), name='wallet-movements'),
]
