from rest_framework import serializers
from .models import ArbitrageOpportunity

class ArbitrageOpportunitySerializer(serializers.ModelSerializer):
    buy_exchange_name = serializers.CharField(source='buy_exchange.name', read_only=True)
    sell_exchange_name = serializers.CharField(source='sell_exchange.name', read_only=True)

    class Meta:
        model = ArbitrageOpportunity
        fields = '__all__'
