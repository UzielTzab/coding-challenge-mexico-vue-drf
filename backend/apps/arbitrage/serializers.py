from rest_framework import serializers
from .models import ArbitrageOpportunity

class ArbitrageOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageOpportunity
        fields = '__all__'
