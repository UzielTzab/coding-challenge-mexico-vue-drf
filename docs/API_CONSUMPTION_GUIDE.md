# API_CONSUMPTION_GUIDE.md

# Guía oficial de consumo de APIs y WebSockets externos

Este documento define cómo el backend de **ArbiBTC** consume datos públicos de mercado desde exchanges externos para detectar oportunidades de arbitraje de Bitcoin en tiempo real.

El sistema utiliza WebSockets públicos para recibir datos de mercado, normalizarlos, almacenarlos como `MarketSnapshot`, ejecutar el motor de arbitraje y enviar eventos internos al frontend mediante Django Channels.

---

## 1. Objetivo del consumo de APIs

El backend debe obtener datos en tiempo real de al menos dos exchanges para comparar precios de BTC entre mercados.

El objetivo mínimo es obtener:

```txt
best_bid
best_ask
bid_volume
ask_volume
symbol
exchange
timestamp
latency_ms
```

Estos valores permiten detectar una oportunidad cuando:

```txt
Ask de Exchange A < Bid de Exchange B
```

Ejemplo:

```txt
Kraken Ask:   69,612.70
Binance Bid: 69,642.10

Si Kraken Ask < Binance Bid:
    existe una oportunidad bruta de arbitraje
```

---

## 2. Exchanges prioritarios

El sistema implementa primero estos exchanges:

```txt
1. Binance
2. Kraken
```

Coinbase queda preparado como tercer exchange, pero no bloquea el MVP.

```txt
3. Coinbase
```

---

## 3. Estrategia de implementación

El consumo de APIs externas no debe implementarse directamente dentro de las views de Django.

El flujo obligatorio es:

```txt
Exchange WebSocket externo
        ↓
Exchange Client
        ↓
Normalizer
        ↓
Market Data Processor
        ↓
MarketSnapshot
        ↓
Arbitrage Engine
        ↓
ArbitrageOpportunity
        ↓
Django Channels
        ↓
Frontend Vue 3
```

---

## 4. Ubicación dentro del backend

Los archivos relacionados con consumo de APIs externas se organizan así:

```txt
backend/
├── apps/
│   ├── exchanges/
│   │   ├── clients/
│   │   │   ├── base_client.py
│   │   │   ├── binance_client.py
│   │   │   ├── kraken_client.py
│   │   │   └── coinbase_client.py
│   │   │
│   │   └── normalizers/
│   │       ├── base_normalizer.py
│   │       ├── binance_normalizer.py
│   │       ├── kraken_normalizer.py
│   │       └── coinbase_normalizer.py
│   │
│   └── market_data/
│       ├── streams/
│       │   ├── stream_manager.py
│       │   ├── binance_stream.py
│       │   ├── kraken_stream.py
│       │   ├── coinbase_stream.py
│       │   └── reconnect_policy.py
│       │
│       ├── processors/
│       │   ├── ticker_processor.py
│       │   ├── order_book_processor.py
│       │   └── latency_processor.py
│       │
│       └── management/
│           └── commands/
│               ├── run_market_streams.py
│               ├── test_binance_ws.py
│               └── test_kraken_ws.py
```

---

## 5. Binance WebSocket

### Uso en el MVP

Binance se implementa con el stream `bookTicker`, porque entrega el mejor bid y ask en tiempo real para un símbolo específico.

### URL WebSocket

```txt
wss://stream.binance.com:9443/ws/btcusdt@bookTicker
```

### Stream

```txt
btcusdt@bookTicker
```

### Símbolo interno

```txt
BTC/USDT
```

### Payload esperado

Binance envía un mensaje similar a:

```json
{
  "u": 400900217,
  "s": "BTCUSDT",
  "b": "69642.10000000",
  "B": "1.24500000",
  "a": "69657.20000000",
  "A": "1.10200000"
}
```

### Mapeo

```txt
s → symbol
b → best_bid
B → bid_volume
a → best_ask
A → ask_volume
```

### Normalización esperada

```python
{
    "exchange_code": "binance",
    "symbol": "BTC/USDT",
    "best_bid": Decimal("69642.10"),
    "bid_volume": Decimal("1.245"),
    "best_ask": Decimal("69657.20"),
    "ask_volume": Decimal("1.102"),
}
```

---

## 6. Kraken WebSocket

### Uso en el MVP

Kraken se implementa inicialmente con el canal `ticker`, porque entrega datos de nivel 1, es decir, top of book: mejor bid y mejor ask.

### URL WebSocket

```txt
wss://ws.kraken.com/v2
```

### Canal

```txt
ticker
```

### Símbolo externo

```txt
BTC/USD
```

> Nota: en algunas versiones/documentación antigua de Kraken puede verse `XBT/USD`. Para WebSocket v2 se usa el formato de símbolos definido por Kraken en su documentación actual. El normalizer debe aceptar variantes si fuera necesario.

### Mensaje de suscripción

```json
{
  "method": "subscribe",
  "params": {
    "channel": "ticker",
    "symbol": [
      "BTC/USD"
    ]
  }
}
```

### Normalización esperada

```python
{
    "exchange_code": "kraken",
    "symbol": "BTC/USD",
    "best_bid": Decimal("69598.40"),
    "bid_volume": Decimal("1.321"),
    "best_ask": Decimal("69612.70"),
    "ask_volume": Decimal("1.213"),
}
```

---

## 7. Coinbase WebSocket

### Estado dentro del proyecto

Coinbase queda preparado como tercer exchange. No es obligatorio para el primer MVP si Binance y Kraken ya funcionan correctamente.

### URL WebSocket

```txt
wss://advanced-trade-ws.coinbase.com
```

### Canales disponibles

Coinbase Advanced Trade ofrece canales como:

```txt
ticker
ticker_batch
level2
market_trades
heartbeats
```

### Canal recomendado para MVP

```txt
ticker
```

### Producto

```txt
BTC-USD
```

### Suscripción conceptual

```json
{
  "type": "subscribe",
  "product_ids": [
    "BTC-USD"
  ],
  "channel": "ticker"
}
```

### Normalización esperada

```python
{
    "exchange_code": "coinbase",
    "symbol": "BTC/USD",
    "best_bid": Decimal("69631.80"),
    "bid_volume": Decimal("1.152"),
    "best_ask": Decimal("69648.30"),
    "ask_volume": Decimal("1.002"),
}
```

---

## 8. Tabla de configuración de exchanges

Los datos de conexión deben vivir en la tabla `Exchange` y también pueden inicializarse mediante seed.

### Modelo `Exchange`

Campos mínimos:

```txt
name
code
is_active
api_base_url
websocket_url
websocket_channel
market_symbol
internal_symbol
trading_fee_percent
withdrawal_fee_btc
supports_websocket
created_at
updated_at
```

### Seed inicial

```python
EXCHANGES = [
    {
        "name": "Binance",
        "code": "binance",
        "websocket_url": "wss://stream.binance.com:9443/ws/btcusdt@bookTicker",
        "websocket_channel": "bookTicker",
        "market_symbol": "BTCUSDT",
        "internal_symbol": "BTC/USDT",
        "trading_fee_percent": "0.10",
        "withdrawal_fee_btc": "0.0005",
        "supports_websocket": True,
        "is_active": True,
    },
    {
        "name": "Kraken",
        "code": "kraken",
        "websocket_url": "wss://ws.kraken.com/v2",
        "websocket_channel": "ticker",
        "market_symbol": "BTC/USD",
        "internal_symbol": "BTC/USD",
        "trading_fee_percent": "0.26",
        "withdrawal_fee_btc": "0.0002",
        "supports_websocket": True,
        "is_active": True,
    },
    {
        "name": "Coinbase",
        "code": "coinbase",
        "websocket_url": "wss://advanced-trade-ws.coinbase.com",
        "websocket_channel": "ticker",
        "market_symbol": "BTC-USD",
        "internal_symbol": "BTC/USD",
        "trading_fee_percent": "0.40",
        "withdrawal_fee_btc": "0.0005",
        "supports_websocket": True,
        "is_active": False,
    },
]
```

---

## 9. Script aislado para probar Binance

Antes de integrar Binance en Django, se prueba de forma aislada.

Archivo:

```txt
backend/scripts/test_binance_ws.py
```

Código:

```python
import asyncio
import json
from decimal import Decimal

import websockets


async def main():
    url = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"

    async with websockets.connect(url) as ws:
        while True:
            message = await ws.recv()
            data = json.loads(message)

            normalized = {
                "exchange": "binance",
                "symbol": "BTC/USDT",
                "best_bid": Decimal(data["b"]),
                "bid_volume": Decimal(data["B"]),
                "best_ask": Decimal(data["a"]),
                "ask_volume": Decimal(data["A"]),
            }

            print(normalized)


if __name__ == "__main__":
    asyncio.run(main())
```

Resultado esperado:

```txt
{
  'exchange': 'binance',
  'symbol': 'BTC/USDT',
  'best_bid': Decimal('69642.10000000'),
  'bid_volume': Decimal('1.24500000'),
  'best_ask': Decimal('69657.20000000'),
  'ask_volume': Decimal('1.10200000')
}
```

---

## 10. Script aislado para probar Kraken

Antes de integrar Kraken en Django, se prueba de forma aislada.

Archivo:

```txt
backend/scripts/test_kraken_ws.py
```

Código:

```python
import asyncio
import json

import websockets


async def main():
    url = "wss://ws.kraken.com/v2"

    subscribe_message = {
        "method": "subscribe",
        "params": {
            "channel": "ticker",
            "symbol": ["BTC/USD"],
        },
    }

    async with websockets.connect(url) as ws:
        await ws.send(json.dumps(subscribe_message))

        while True:
            message = await ws.recv()
            data = json.loads(message)
            print(data)


if __name__ == "__main__":
    asyncio.run(main())
```

Resultado esperado:

```txt
Mensajes de suscripción, heartbeats y actualizaciones del ticker BTC/USD.
```

---

## 11. Cliente base de WebSocket

Todos los clientes externos deben heredar de una base común.

Archivo:

```txt
backend/apps/exchanges/clients/base_client.py
```

Responsabilidades:

```txt
Abrir conexión WebSocket
Cerrar conexión WebSocket
Reintentar conexión
Recibir mensajes
Enviar mensajes de suscripción cuando aplique
Reportar errores
```

Interfaz base:

```python
from abc import ABC, abstractmethod


class BaseExchangeWebSocketClient(ABC):
    exchange_code: str
    websocket_url: str

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def subscribe(self):
        pass

    @abstractmethod
    async def listen(self):
        pass

    @abstractmethod
    async def normalize_message(self, raw_message: dict):
        pass
```

---

## 12. Normalizers

Los normalizers eliminan diferencias entre exchanges.

### Regla

Ningún dato crudo de Binance, Kraken o Coinbase debe entrar directamente al motor de arbitraje.

Todo debe convertirse primero a este contrato:

```python
{
    "exchange_code": str,
    "symbol": str,
    "best_bid": Decimal,
    "best_ask": Decimal,
    "bid_volume": Decimal,
    "ask_volume": Decimal,
    "exchange_timestamp": datetime | None,
    "received_at": datetime,
    "latency_ms": int,
}
```

---

## 13. Guardado en MarketSnapshot

Después de normalizar un mensaje, se guarda o actualiza un `MarketSnapshot`.

Modelo:

```txt
MarketSnapshot
```

Campos mínimos:

```txt
exchange
symbol
best_bid
best_ask
bid_volume
ask_volume
spread
spread_percent
latency_ms
exchange_timestamp
received_at
created_at
```

Cálculos:

```txt
spread = best_ask - best_bid
spread_percent = (spread / best_bid) * 100
```

---

## 14. Disparo del motor de arbitraje

Cada vez que se guarda un snapshot válido:

```txt
1. Se actualiza MarketSnapshot.
2. Se consulta el último snapshot de los demás exchanges.
3. Se compara Ask del exchange actual contra Bid de los otros exchanges.
4. Se compara Bid del exchange actual contra Ask de los otros exchanges.
5. Se calcula rentabilidad neta.
6. Se crea ArbitrageOpportunity.
7. Si cumple umbral, se marca como profitable.
8. Si no cumple, se marca como discarded.
9. Se emite evento interno al frontend.
```

---

## 15. Comparación entre USD y USDT

El MVP permite comparar:

```txt
BTC/USDT
BTC/USD
```

Regla del proyecto:

```txt
Para la simulación del challenge, USD y USDT se tratan como equivalentes 1:1.
```

Esta decisión debe documentarse en README:

```md
Para simplificar el MVP, el sistema normaliza BTC/USD y BTC/USDT bajo un valor equivalente USD≈USDT. Esta decisión permite demostrar la arquitectura de arbitraje sin introducir una capa adicional de conversión stablecoin/fiat. En una versión productiva se integraría conversión FX/stablecoin y riesgos de depeg.
```

---

## 16. Comando principal de streams

Archivo:

```txt
backend/apps/market_data/management/commands/run_market_streams.py
```

Responsabilidad:

```txt
Ejecutar conexiones WebSocket externas activas.
Mantener los streams vivos.
Reintentar conexión si un exchange falla.
Registrar logs de estado.
Enviar snapshots al motor de arbitraje.
```

Uso:

```bash
python manage.py run_market_streams
```

---

## 17. Política de reconexión

Archivo:

```txt
backend/apps/market_data/streams/reconnect_policy.py
```

Reglas:

```txt
1. Reintentar conexión automáticamente si el WebSocket cae.
2. Esperar 1 segundo antes del primer reintento.
3. Incrementar espera progresivamente hasta un máximo de 30 segundos.
4. Registrar cada intento en SystemLog.
5. Si se supera el máximo de errores consecutivos, activar warning.
6. Si todos los exchanges fallan, activar circuit breaker.
```

---

## 18. Eventos internos hacia frontend

Cuando el backend recibe datos externos, debe emitir eventos internos mediante Django Channels.

Canales internos:

```txt
/ws/dashboard/
/ws/market/
/ws/opportunities/
/ws/logs/
```

Eventos:

```txt
market_update
opportunity_detected
opportunity_updated
trade_simulated
wallet_updated
system_log_created
bot_status_changed
```

Ejemplo:

```json
{
  "type": "market_update",
  "payload": {
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "best_bid": "69642.10",
    "best_ask": "69657.20",
    "bid_volume": "1.245",
    "ask_volume": "1.102",
    "latency_ms": 28,
    "received_at": "2026-05-29T14:32:18Z"
  }
}
```

---

## 19. Orden obligatorio de implementación

La implementación se realiza en este orden:

```txt
1. Probar Binance en script aislado.
2. Probar Kraken en script aislado.
3. Crear modelo Exchange.
4. Crear seed de exchanges.
5. Crear normalizer de Binance.
6. Crear normalizer de Kraken.
7. Crear MarketSnapshot.
8. Guardar mensajes normalizados en MarketSnapshot.
9. Crear run_market_streams.
10. Ejecutar ambos streams juntos.
11. Crear ArbitrageEngine.
12. Detectar oportunidades con snapshots reales.
13. Crear eventos internos con Django Channels.
14. Conectar frontend a /ws/dashboard/.
15. Agregar Coinbase si queda tiempo.
```

---

## 20. Checklist de validación

Antes de considerar terminado el consumo de APIs externas, debe cumplirse:

```txt
Binance conecta por WebSocket.
Kraken conecta por WebSocket.
Los mensajes crudos se imprimen correctamente.
Los mensajes se normalizan a un contrato común.
Se guardan MarketSnapshot en base de datos.
Se calcula spread interno por exchange.
Se detectan oportunidades entre exchanges.
Se registran SystemLogs de conexión.
El frontend recibe market_update.
El frontend recibe opportunity_detected.
El bot continúa funcionando si un exchange se reconecta.
```

---

## 21. Dependencias backend necesarias

Agregar en `requirements/base.txt`:

```txt
websockets
channels
daphne
```

Si se usa Redis para Channels en producción:

```txt
channels-redis
redis
```

---

## 22. Notas técnicas importantes

### No usar floats

Todos los cálculos financieros deben usar `Decimal`.

Correcto:

```python
from decimal import Decimal

price = Decimal("69642.10")
```

Incorrecto:

```python
price = 69642.10
```

### No guardar cada tick sin control

Los WebSockets pueden enviar muchos mensajes. Para el MVP se permite guardar snapshots recientes, pero si el volumen crece, se debe:

```txt
Actualizar último snapshot
Guardar histórico reducido
Limpiar datos antiguos
Agregar throttling
```

### No bloquear el event loop

El procesamiento debe ser rápido. Si una tarea es pesada, se mueve a worker o se desacopla.

### No mezclar APIs externas con WebSockets internos

```txt
WebSockets externos:
Binance, Kraken, Coinbase → Backend

WebSockets internos:
Backend → Frontend Vue 3
```

---

## 23. Referencias oficiales

- Binance Spot WebSocket Streams: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
- Kraken WebSocket API Ticker v2: https://docs.kraken.com/api/docs/websocket-v2/ticker
- Kraken API Center: https://docs.kraken.com/
- Coinbase Advanced Trade WebSocket Overview: https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/websocket/websocket-overview
- Coinbase Advanced Trade WebSocket Channels: https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/websocket/websocket-channels

---

## 24. Resultado esperado

Al terminar esta parte, el backend debe poder mostrar en consola:

```txt
[binance] bid=69642.10 ask=69657.20
[kraken]  bid=69598.40 ask=69612.70
```

Y el frontend debe recibir eventos como:

```txt
market_update
opportunity_detected
system_log_created
```

Esta etapa convierte el proyecto de una maqueta a un sistema vivo de arbitraje en tiempo real.
