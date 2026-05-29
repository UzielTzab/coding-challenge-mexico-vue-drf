from django.urls import path
from .views import TradeListView, TradeSummaryView

urlpatterns = [
    path('', TradeListView.as_view(), name='trade-list'),
    path('summary/', TradeSummaryView.as_view(), name='trade-summary'),
]
