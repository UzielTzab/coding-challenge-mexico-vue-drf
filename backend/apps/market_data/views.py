from rest_framework import generics
from .models import MarketSnapshot
from .serializers import MarketSnapshotSerializer

class MarketSnapshotLatestView(generics.ListAPIView):
    serializer_class = MarketSnapshotSerializer

    def get_queryset(self):
        return MarketSnapshot.objects.order_by('-received_at')[:10]
