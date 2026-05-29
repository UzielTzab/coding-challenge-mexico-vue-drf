# WEBSOCKET_EVENTS.md

# Contrato oficial WebSocket — ArbiBTC

Este documento define los eventos WebSocket que el backend emite y el frontend consume. Los WebSockets son parte central del sistema porque el dashboard debe mostrar actividad en tiempo real.

---

## 1. Endpoint WebSocket

Local:

```txt
ws://localhost:8000/ws/dashboard/
```

Producción:

```txt
wss://<backend-domain>/ws/dashboard/
```

---

## 2. Formato estándar de evento

Todos los eventos siguen esta estructura:

```json
{
  "type": "event_name",
  "timestamp": "2026-05-29T14:32:18Z",
  "payload": {}
}
```

---

## 3. Eventos oficiales

```txt
bot_status
market_update
opportunity_detected
opportunity_updated
trade_simulated
wallet_updated
performance_updated
system_log
heartbeat
error
```

---

## 4. bot_status

Se emite cuando cambia el estado del bot.

```json
{
  "type": "bot_status",
  "timestamp": "2026-05-29T14:32:18Z",
  "payload": {
    "status": "running",
    "mode": "simulation",
    "backend": "online",
    "market_feeds": "online",
    "strategy_engine": "active",
    "database": "connected"
  }
}
```

Estados:

```txt
running
paused
stopped
error
```

---

## 5. market_update

Se emite cuando llega un nuevo snapshot de mercado.

```json
{
  "type": "market_update",
  "timestamp": "2026-05-29T14:32:18Z",
  "payload": {
    "exchange": "Binance",
    "exchange_code": "binance",
    "symbol": "BTC/USDT",
    "best_bid": "69642.10",
    "best_ask": "69657.20",
    "bid_volume": "1.24500000",
    "ask_volume": "1.10200000",
    "spread": "15.10",
    "latency_ms": 28,
    "received_at": "2026-05-29T14:32:18Z"
  }
}
```

Frontend:

- Actualiza `market.store.ts`.
- Refresca `ExchangeCard.vue`.
- Actualiza latencia del header.

---

## 6. opportunity_detected

Se emite cuando el motor detecta una nueva oportunidad.

```json
{
  "type": "opportunity_detected",
  "timestamp": "2026-05-29T14:32:15Z",
  "payload": {
    "id": "uuid",
    "symbol": "BTC/USDT",
    "buy_exchange": "Kraken",
    "sell_exchange": "Binance",
    "ask_price": "69612.70",
    "bid_price": "69642.10",
    "volume_available": "0.84200000",
    "gross_spread": "29.40",
    "gross_spread_percent": "0.0422",
    "estimated_fees": "15.42",
    "estimated_slippage": "6.73",
    "latency_penalty": "1.52",
    "net_profit": "18.74",
    "net_profit_percent": "0.0270",
    "status": "profitable",
    "decision_reason": "Ejecutar porque la ganancia neta supera el umbral mínimo."
  }
}
```

Frontend:

- Inserta la oportunidad al inicio de la tabla.
- Actualiza contadores KPI.
- Muestra highlight si es rentable.

---

## 7. opportunity_updated

Se emite cuando una oportunidad cambia de estado.

```json
{
  "type": "opportunity_updated",
  "timestamp": "2026-05-29T14:32:17Z",
  "payload": {
    "id": "uuid",
    "status": "executed",
    "decision_reason": "La oportunidad fue ejecutada mediante simulación."
  }
}
```

---

## 8. trade_simulated

Se emite cuando una operación simulada se completa.

```json
{
  "type": "trade_simulated",
  "timestamp": "2026-05-29T14:32:17Z",
  "payload": {
    "id": "uuid",
    "opportunity_id": "uuid",
    "symbol": "BTC/USDT",
    "buy_exchange": "Kraken",
    "sell_exchange": "Binance",
    "requested_quantity_btc": "1.00000000",
    "executed_quantity_btc": "0.42000000",
    "buy_cost": "29245.33",
    "sell_revenue": "29210.25",
    "total_fees": "35.09",
    "slippage_cost": "6.73",
    "latency_cost": "1.52",
    "net_profit": "26.80",
    "status": "partially_executed"
  }
}
```

Frontend:

- Actualiza tabla de operaciones.
- Actualiza panel de ejecución.
- Actualiza P&L.
- Actualiza logs.

---

## 9. wallet_updated

Se emite cuando una wallet cambia.

```json
{
  "type": "wallet_updated",
  "timestamp": "2026-05-29T14:32:17Z",
  "payload": {
    "exchange": "Binance",
    "btc_available": "1.23456700",
    "usdt_available": "15432.21",
    "btc_locked": "0.05000000",
    "usdt_locked": "0.00",
    "total_value_usd": "101265.43"
  }
}
```

---

## 10. performance_updated

Se emite después de una oportunidad o trade que modifica métricas.

```json
{
  "type": "performance_updated",
  "timestamp": "2026-05-29T14:32:17Z",
  "payload": {
    "pnl_accumulated": "1246.38",
    "win_rate": "62.10",
    "average_profit": "69.24",
    "total_opportunities": 29,
    "executed": 18,
    "discarded": 10,
    "failed": 1
  }
}
```

---

## 11. system_log

Se emite cuando se registra un log técnico.

```json
{
  "type": "system_log",
  "timestamp": "2026-05-29T14:32:18Z",
  "payload": {
    "level": "info",
    "source": "market_data",
    "message": "WebSocket Binance conectado",
    "metadata": {}
  }
}
```

Niveles:

```txt
info
success
warn
error
```

---

## 12. heartbeat

Se emite periódicamente para mantener viva la conexión.

```json
{
  "type": "heartbeat",
  "timestamp": "2026-05-29T14:32:18Z",
  "payload": {
    "latency_ms": 28,
    "server_time": "2026-05-29T14:32:18Z"
  }
}
```

Frontend:

- Calcula latencia.
- Actualiza indicador de conexión.

---

## 13. error

Se emite ante errores controlados.

```json
{
  "type": "error",
  "timestamp": "2026-05-29T14:32:18Z",
  "payload": {
    "code": "MARKET_FEED_DISCONNECTED",
    "message": "El feed de Kraken se desconectó. Intentando reconectar."
  }
}
```

---

## 14. Reglas frontend para WebSocket

El frontend implementa `useDashboardSocket.ts` y nunca abre WebSockets directamente desde componentes visuales.

El composable debe:

- Conectar al endpoint oficial.
- Reintentar conexión automáticamente.
- Procesar eventos por `type`.
- Enviar eventos a stores.
- Exponer estado de conexión.
- Cerrar conexión al desmontar AppShell si corresponde.

---

## 15. Reglas backend para WebSocket

El backend implementa `DashboardConsumer` con Django Channels.

El backend emite eventos después de:

- Recibir market data.
- Detectar oportunidad.
- Simular trade.
- Actualizar wallet.
- Registrar log.
- Actualizar métricas.

---

## 16. Criterio de aceptación

WebSocket está correcto cuando:

- El dashboard recibe `heartbeat`.
- Las cards de exchanges se actualizan con `market_update`.
- La tabla de oportunidades recibe `opportunity_detected`.
- El panel de operaciones recibe `trade_simulated`.
- Las wallets reciben `wallet_updated`.
- Los logs reciben `system_log`.
