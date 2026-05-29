import asyncio
from django.core.management.base import BaseCommand
from apps.market_data.streams.stream_manager import StreamManager

class Command(BaseCommand):
    help = 'Inicia los websockets para consumir datos de mercado (Binance, Kraken, etc)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Market Streams (Binance & Kraken)..."))
        
        manager = StreamManager()
        
        try:
            asyncio.run(manager.start())
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Streams detenidos manualmente."))
