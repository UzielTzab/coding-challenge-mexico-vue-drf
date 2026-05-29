from rest_framework import serializers
from .models import SimulatedTrade

class SimulatedTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatedTrade
        fields = '__all__'
