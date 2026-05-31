from rest_framework import serializers
from .models import Wallet, WalletMovement

class WalletSerializer(serializers.ModelSerializer):
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'

class WalletMovementSerializer(serializers.ModelSerializer):
    wallet_exchange = serializers.CharField(source='wallet.exchange.name', read_only=True)

    class Meta:
        model = WalletMovement
        fields = '__all__'
