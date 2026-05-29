from django.urls import path
from .views import MarketSnapshotLatestView

urlpatterns = [
    path('snapshots/latest/', MarketSnapshotLatestView.as_view(), name='market-snapshots-latest'),
]
