from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)

    class Meta:
        model = Wallet
        fields = '__all__'
