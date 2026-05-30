import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.trading.models import SimulatedTrade
from apps.arbitrage.models import ArbitrageOpportunity
from apps.analytics.models import PerformanceSnapshot
from apps.wallets.models import WalletMovement, Wallet

def clean_database():
    print("Iniciando limpieza de la base de datos...")
    
    # Eliminar datos históricos
    deleted_trades, _ = SimulatedTrade.objects.all().delete()
    print(f"- Eliminados {deleted_trades} registros de SimulatedTrade")
    
    deleted_opportunities, _ = ArbitrageOpportunity.objects.all().delete()
    print(f"- Eliminados {deleted_opportunities} registros de ArbitrageOpportunity")
    
    deleted_snapshots, _ = PerformanceSnapshot.objects.all().delete()
    print(f"- Eliminados {deleted_snapshots} registros de PerformanceSnapshot")
    
    deleted_movements, _ = WalletMovement.objects.all().delete()
    print(f"- Eliminados {deleted_movements} registros de WalletMovement")
    
    # Reiniciar balances de las wallets
    updated_wallets = Wallet.objects.update(btc_available=5.0, usdt_available=100000.0)
    print(f"- Reiniciados los balances de {updated_wallets} Wallets a 5.0 BTC y 100,000 USDT")
    
    print("\n¡Limpieza completada exitosamente!")

if __name__ == '__main__':
    clean_database()
