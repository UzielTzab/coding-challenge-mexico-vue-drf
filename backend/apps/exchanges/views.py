from rest_framework import generics
from .models import Exchange
from .serializers import ExchangeSerializer

class ExchangeListView(generics.ListAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
