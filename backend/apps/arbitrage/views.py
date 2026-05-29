from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import ArbitrageOpportunity
from .serializers import ArbitrageOpportunitySerializer

class OpportunityListView(generics.ListAPIView):
    queryset = ArbitrageOpportunity.objects.all().order_by('-detected_at')
    serializer_class = ArbitrageOpportunitySerializer

class OpportunitySummaryView(APIView):
    def get(self, request):
        total = ArbitrageOpportunity.objects.count()
        profitable = ArbitrageOpportunity.objects.filter(status='profitable').count()
        executed = ArbitrageOpportunity.objects.filter(status='executed').count()
        discarded = ArbitrageOpportunity.objects.filter(status='discarded').count()
        profit = ArbitrageOpportunity.objects.filter(status='executed').aggregate(Sum('net_profit'))['net_profit__sum'] or 0
        return Response({
            "total_detected": total,
            "profitable": profitable,
            "discarded": discarded,
            "executed": executed,
            "potential_profit_usd": profit
        })
