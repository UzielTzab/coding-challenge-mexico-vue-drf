from rest_framework import serializers
from .models import MarketSnapshot

class MarketSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketSnapshot
        fields = '__all__'
