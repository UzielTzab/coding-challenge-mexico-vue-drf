from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer

class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
