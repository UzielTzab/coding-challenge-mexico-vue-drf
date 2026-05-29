from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg
from .models import SimulatedTrade
from .serializers import SimulatedTradeSerializer

class TradeListView(generics.ListAPIView):
    queryset = SimulatedTrade.objects.all().order_by('-executed_at')
    serializer_class = SimulatedTradeSerializer

class TradeSummaryView(APIView):
    def get(self, request):
        total = SimulatedTrade.objects.count()
        profitable = SimulatedTrade.objects.filter(net_profit__gt=0).count()
        partial = SimulatedTrade.objects.filter(status='partially_executed').count()
        profit_sum = SimulatedTrade.objects.aggregate(Sum('net_profit'))['net_profit__sum'] or 0
        avg_profit = SimulatedTrade.objects.aggregate(Avg('net_profit'))['net_profit__avg'] or 0
        return Response({
            "total_trades": total,
            "profitable_trades": profitable,
            "partial_trades": partial,
            "total_net_profit_usd": profit_sum,
            "average_profit_per_trade_usd": avg_profit
        })
