import os

base_dir = r'C:\Users\uzieltzab\Documents\ChallengeMexico\coding_challenge_mexico\backend\apps'

# health
with open(os.path.join(base_dir, 'health', 'views.py'), 'w') as f:
    f.write('''from rest_framework.views import APIView
from rest_framework.response import Response

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "ArbiBTC API"})
''')

with open(os.path.join(base_dir, 'health', 'urls.py'), 'w') as f:
    f.write('''from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    path('', HealthCheckView.as_view(), name='health-check'),
]
''')

# exchanges
with open(os.path.join(base_dir, 'exchanges', 'serializers.py'), 'w') as f:
    f.write('''from rest_framework import serializers
from .models import Exchange

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'
''')

with open(os.path.join(base_dir, 'exchanges', 'views.py'), 'w') as f:
    f.write('''from rest_framework import generics
from .models import Exchange
from .serializers import ExchangeSerializer

class ExchangeListView(generics.ListAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
''')

with open(os.path.join(base_dir, 'exchanges', 'urls.py'), 'w') as f:
    f.write('''from django.urls import path
from .views import ExchangeListView

urlpatterns = [
    path('', ExchangeListView.as_view(), name='exchange-list'),
]
''')

# market_data
with open(os.path.join(base_dir, 'market_data', 'serializers.py'), 'w') as f:
    f.write('''from rest_framework import serializers
from .models import MarketSnapshot

class MarketSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketSnapshot
        fields = '__all__'
''')

with open(os.path.join(base_dir, 'market_data', 'views.py'), 'w') as f:
    f.write('''from rest_framework import generics
from .models import MarketSnapshot
from .serializers import MarketSnapshotSerializer

class MarketSnapshotLatestView(generics.ListAPIView):
    serializer_class = MarketSnapshotSerializer

    def get_queryset(self):
        return MarketSnapshot.objects.order_by('-received_at')[:10]
''')

with open(os.path.join(base_dir, 'market_data', 'urls.py'), 'w') as f:
    f.write('''from django.urls import path
from .views import MarketSnapshotLatestView

urlpatterns = [
    path('snapshots/latest/', MarketSnapshotLatestView.as_view(), name='market-snapshots-latest'),
]
''')

# arbitrage
with open(os.path.join(base_dir, 'arbitrage', 'serializers.py'), 'w') as f:
    f.write('''from rest_framework import serializers
from .models import ArbitrageOpportunity

class ArbitrageOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageOpportunity
        fields = '__all__'
''')

with open(os.path.join(base_dir, 'arbitrage', 'views.py'), 'w') as f:
    f.write('''from rest_framework import generics
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
''')

with open(os.path.join(base_dir, 'arbitrage', 'urls.py'), 'w') as f:
    f.write('''from django.urls import path
from .views import OpportunityListView, OpportunitySummaryView

urlpatterns = [
    path('', OpportunityListView.as_view(), name='opportunity-list'),
    path('summary/', OpportunitySummaryView.as_view(), name='opportunity-summary'),
]
''')

# trading
with open(os.path.join(base_dir, 'trading', 'serializers.py'), 'w') as f:
    f.write('''from rest_framework import serializers
from .models import SimulatedTrade

class SimulatedTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatedTrade
        fields = '__all__'
''')

with open(os.path.join(base_dir, 'trading', 'views.py'), 'w') as f:
    f.write('''from rest_framework import generics
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
''')

with open(os.path.join(base_dir, 'trading', 'urls.py'), 'w') as f:
    f.write('''from django.urls import path
from .views import TradeListView, TradeSummaryView

urlpatterns = [
    path('', TradeListView.as_view(), name='trade-list'),
    path('summary/', TradeSummaryView.as_view(), name='trade-summary'),
]
''')

# wallets
with open(os.path.join(base_dir, 'wallets', 'serializers.py'), 'w') as f:
    f.write('''from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
''')

with open(os.path.join(base_dir, 'wallets', 'views.py'), 'w') as f:
    f.write('''from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer

class WalletListView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
''')

with open(os.path.join(base_dir, 'wallets', 'urls.py'), 'w') as f:
    f.write('''from django.urls import path
from .views import WalletListView

urlpatterns = [
    path('', WalletListView.as_view(), name='wallet-list'),
]
''')

# system_logs
with open(os.path.join(base_dir, 'system_logs', 'serializers.py'), 'w') as f:
    f.write('''from rest_framework import serializers
from .models import SystemLog

class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = '__all__'
''')

with open(os.path.join(base_dir, 'system_logs', 'views.py'), 'w') as f:
    f.write('''from rest_framework import generics
from .models import SystemLog
from .serializers import SystemLogSerializer

class SystemLogListView(generics.ListAPIView):
    queryset = SystemLog.objects.all().order_by('-created_at')
    serializer_class = SystemLogSerializer
''')

with open(os.path.join(base_dir, 'system_logs', 'urls.py'), 'w') as f:
    f.write('''from django.urls import path
from .views import SystemLogListView

urlpatterns = [
    path('', SystemLogListView.as_view(), name='log-list'),
]
''')
