from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ArbitrageOpportunity
from rest_framework import serializers

class ArbitrageOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageOpportunity
        fields = '__all__'

class ArbitrageOpportunityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArbitrageOpportunity.objects.all().order_by('-detected_at')
    serializer_class = ArbitrageOpportunitySerializer

    @action(detail=True, methods=['post'])
    def simulate(self, request, pk=None):
        opp = self.get_object()
        # Logic for simulation execution will go here
        return Response({"status": "success", "message": "Simulation triggered for opportunity", "opportunity_id": opp.id})
