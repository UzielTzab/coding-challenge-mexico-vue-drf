from rest_framework import generics
from .models import Wallet, WalletMovement
from .serializers import WalletSerializer, WalletMovementSerializer

class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class WalletMovementListView(generics.ListAPIView):
    queryset = WalletMovement.objects.all().order_by('-created_at')
    serializer_class = WalletMovementSerializer
