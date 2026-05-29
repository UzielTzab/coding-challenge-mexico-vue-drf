# API_CONTRACT.md

# Contrato oficial REST API — ArbiBTC

Este documento define los endpoints REST que el frontend consumirá. Todo cambio en la API debe respetar este contrato o actualizar este documento antes de modificar frontend/backend.

Base URL local:

```txt
http://localhost:8000/api
```

Base URL producción:

```txt
https://<backend-domain>/api
```

---

## 1. Convenciones generales

Todas las respuestas usan JSON.

Fechas en formato ISO 8601.

Montos financieros como string decimal para evitar pérdida de precisión.

Ejemplo:

```json
{
  "net_profit": "26.80",
  "quantity_btc": "0.42000000"
}
```

---

## 2. Health check

### GET `/health/`

Respuesta:

```json
{
  "status": "ok",
  "service": "ArbiBTC API",
  "database": "connected",
  "websocket_engine": "enabled"
}
```

---

## 3. Exchanges

### GET `/exchanges/`

Respuesta:

```json
[
  {
    "id": "uuid",
    "name": "Binance",
    "code": "binance",
    "is_active": true,
    "trading_fee_percent": "0.0010",
    "withdrawal_fee_btc": "0.00050000"
  }
]
```

---

## 4. Market snapshots

### GET `/market/snapshots/latest/`

Devuelve el último snapshot por exchange y símbolo.

Respuesta:

```json
[
  {
    "exchange": {
      "id": "uuid",
      "name": "Binance",
      "code": "binance"
    },
    "symbol": "BTC/USDT",
    "best_bid": "69642.10",
    "best_ask": "69657.20",
    "bid_volume": "1.24500000",
    "ask_volume": "1.10200000",
    "spread": "15.10",
    "latency_ms": 28,
    "received_at": "2026-05-29T14:32:18Z"
  }
]
```

---

## 5. Oportunidades

### GET `/opportunities/`

Query params:

| Param | Uso |
|---|---|
| `status` | Filtra por estado. |
| `buy_exchange` | Código exchange compra. |
| `sell_exchange` | Código exchange venta. |
| `min_profit` | Ganancia mínima. |
| `date_from` | Fecha inicial. |
| `date_to` | Fecha final. |

Respuesta:

```json
{
  "count": 24,
  "results": [
    {
      "id": "uuid",
      "detected_at": "2026-05-29T14:32:15Z",
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
  ]
}
```

### GET `/opportunities/summary/`

Respuesta:

```json
{
  "total_detected": 24,
  "profitable": 12,
  "discarded": 10,
  "executed": 2,
  "potential_profit": "248.35"
}
```

### GET `/opportunities/{id}/`

Devuelve el detalle completo para drawer lateral.

### POST `/opportunities/{id}/simulate/`

Ejecuta simulación sobre la oportunidad.

Request:

```json
{
  "quantity_btc": "0.42000000"
}
```

Respuesta:

```json
{
  "trade_id": "uuid",
  "status": "partially_executed",
  "executed_quantity_btc": "0.42000000",
  "net_profit": "26.80",
  "message": "Simulación ejecutada parcialmente."
}
```

---

## 6. Trades simulados

### GET `/trades/`

Respuesta:

```json
{
  "count": 18,
  "results": [
    {
      "id": "uuid",
      "executed_at": "2026-05-29T14:32:17Z",
      "symbol": "BTC/USDT",
      "buy_exchange": "Kraken",
      "sell_exchange": "Binance",
      "executed_quantity_btc": "0.42000000",
      "buy_cost": "29245.33",
      "sell_revenue": "29210.25",
      "total_fees": "35.09",
      "net_profit": "26.80",
      "status": "partially_executed"
    }
  ]
}
```

### GET `/trades/summary/`

Respuesta:

```json
{
  "total_trades": 18,
  "profitable_trades": 14,
  "partial_trades": 3,
  "failed_trades": 1,
  "net_profit_total": "1246.38",
  "average_profit": "69.24"
}
```

---

## 7. Wallets

### GET `/wallets/`

Respuesta:

```json
[
  {
    "exchange": "Binance",
    "btc_available": "1.23456700",
    "usdt_available": "15432.21",
    "btc_locked": "0.05000000",
    "usdt_locked": "0.00",
    "total_value_usd": "101265.43",
    "updated_at": "2026-05-29T14:32:18Z"
  }
]
```

### GET `/wallet-movements/`

Respuesta:

```json
{
  "count": 50,
  "results": [
    {
      "id": "uuid",
      "created_at": "2026-05-29T14:32:17Z",
      "exchange": "Binance",
      "movement_type": "sell",
      "asset": "USDT",
      "amount": "29210.25",
      "balance_before": "12500.00",
      "balance_after": "41710.25",
      "reference": "Simulated trade uuid"
    }
  ]
}
```

---

## 8. Analytics

### GET `/analytics/performance/`

Respuesta:

```json
{
  "pnl_accumulated": "1246.38",
  "win_rate": "62.10",
  "average_execution_time_ms": 2380,
  "average_profit": "69.24",
  "total_fees": "312.42",
  "profit_by_exchange_pair": [
    {
      "pair": "Kraken → Binance",
      "profit": "812.45"
    }
  ],
  "opportunities_by_status": {
    "executed": 18,
    "discarded": 10,
    "failed": 1
  },
  "pnl_series": [
    {
      "time": "14:00",
      "value": "850.00"
    }
  ]
}
```

---

## 9. Logs

### GET `/logs/`

Query params:

| Param | Uso |
|---|---|
| `level` | `info`, `success`, `warn`, `error`. |
| `source` | Módulo origen. |

Respuesta:

```json
{
  "count": 100,
  "results": [
    {
      "id": "uuid",
      "created_at": "2026-05-29T14:32:18Z",
      "level": "info",
      "source": "market_data",
      "message": "WebSocket Binance conectado",
      "metadata": {}
    }
  ]
}
```

---

## 10. Settings

### GET `/settings/`

Respuesta:

```json
{
  "min_profit_percent": "0.20",
  "max_trade_size_btc": "1.50000000",
  "min_volume_btc": "0.10000000",
  "slippage_model": "dynamic_volume",
  "max_latency_ms": 500,
  "daily_max_loss_usd": "1000.00",
  "circuit_breaker_enabled": true,
  "max_trades_per_minute": 10,
  "pause_on_feed_disconnect": true
}
```

### PATCH `/settings/`

Actualiza parámetros de configuración.

---

## 11. Bot control

### POST `/bot/start/`

Respuesta:

```json
{
  "status": "running",
  "message": "Bot iniciado en modo simulación."
}
```

### POST `/bot/pause/`

Respuesta:

```json
{
  "status": "paused",
  "message": "Bot pausado."
}
```

### POST `/bot/stop/`

Respuesta:

```json
{
  "status": "stopped",
  "message": "Bot detenido."
}
```

---

## 12. Códigos de error

```json
{
  "error": "INSUFFICIENT_BALANCE",
  "message": "La wallet del exchange comprador no tiene USDT suficiente."
}
```

Errores oficiales:

```txt
INSUFFICIENT_BALANCE
INSUFFICIENT_LIQUIDITY
OPPORTUNITY_NOT_PROFITABLE
MARKET_DATA_STALE
BOT_PAUSED
VALIDATION_ERROR
INTERNAL_ERROR
```
