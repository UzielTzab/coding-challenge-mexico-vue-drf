# BACKEND_MODELS_GUIDE.md

# Modelos oficiales backend — ArbiBTC

Este documento define los modelos que el backend implementará en Django. Los modelos están diseñados para cubrir dashboard, oportunidades, operaciones, wallets, rendimiento, logs y configuración del bot.

---

## 1. Apps oficiales

```txt
backend/apps/
├── exchanges/
├── market_data/
├── arbitrage/
├── trading/
├── wallets/
├── analytics/
├── system_logs/
└── bot_config/
```

---

## 2. Exchange

App:

```txt
exchanges
```

Modelo:

```txt
Exchange
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `name` | CharField | Nombre visible. |
| `code` | CharField unique | Código interno: `binance`, `kraken`, `coinbase`. |
| `base_url` | URLField | API REST pública. |
| `websocket_url` | URLField | WebSocket público. |
| `trading_fee_percent` | DecimalField | Fee de trading. |
| `withdrawal_fee_btc` | DecimalField | Fee estimado de retiro BTC. |
| `is_active` | BooleanField | Habilita o deshabilita exchange. |
| `created_at` | DateTimeField | Creación. |
| `updated_at` | DateTimeField | Actualización. |

Relaciones:

- Un exchange tiene muchos market snapshots.
- Un exchange puede ser origen de compra en oportunidades.
- Un exchange puede ser destino de venta en oportunidades.
- Un exchange tiene una wallet simulada.

---

## 3. MarketSnapshot

App:

```txt
market_data
```

Modelo:

```txt
MarketSnapshot
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `exchange` | ForeignKey | Exchange origen. |
| `symbol` | CharField | Par normalizado, por ejemplo `BTC/USDT`. |
| `best_bid` | DecimalField | Mejor precio comprador. |
| `best_ask` | DecimalField | Mejor precio vendedor. |
| `bid_volume` | DecimalField | Volumen disponible en bid. |
| `ask_volume` | DecimalField | Volumen disponible en ask. |
| `spread` | DecimalField | Spread interno del exchange. |
| `latency_ms` | PositiveIntegerField | Latencia medida. |
| `raw_payload` | JSONField | Payload original resumido. |
| `received_at` | DateTimeField | Momento de recepción. |
| `created_at` | DateTimeField | Momento de persistencia. |

Índices:

- `exchange`, `symbol`, `received_at`.
- `symbol`, `received_at`.

Uso:

- Dashboard de mercados.
- Detección de oportunidades.
- Cálculo de latencia.

---

## 4. ArbitrageOpportunity

App:

```txt
arbitrage
```

Modelo:

```txt
ArbitrageOpportunity
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `symbol` | CharField | Par operado. |
| `buy_exchange` | ForeignKey Exchange | Exchange donde se compra. |
| `sell_exchange` | ForeignKey Exchange | Exchange donde se vende. |
| `ask_price` | DecimalField | Precio de compra. |
| `bid_price` | DecimalField | Precio de venta. |
| `volume_available` | DecimalField | Volumen máximo ejecutable. |
| `gross_spread` | DecimalField | Diferencia bruta en USD. |
| `gross_spread_percent` | DecimalField | Diferencia bruta en %. |
| `estimated_fees` | DecimalField | Fees estimados. |
| `estimated_slippage` | DecimalField | Slippage estimado. |
| `withdrawal_fee` | DecimalField | Fee estimado de retiro. |
| `latency_penalty` | DecimalField | Penalización por latencia. |
| `net_profit` | DecimalField | Ganancia neta estimada. |
| `net_profit_percent` | DecimalField | Ganancia neta %. |
| `status` | CharField choices | Estado de oportunidad. |
| `decision_reason` | TextField | Explicación de decisión. |
| `detected_at` | DateTimeField | Momento de detección. |
| `created_at` | DateTimeField | Momento de guardado. |

Estados oficiales:

```txt
detected
profitable
discarded
executed
failed
```

Regla:

- Si `net_profit_percent` supera el umbral configurado y existe liquidez, el estado será `profitable`.
- Si no supera el umbral, el estado será `discarded`.
- Si se simula una operación sobre ella, el estado pasa a `executed`.

---

## 5. SimulatedTrade

App:

```txt
trading
```

Modelo:

```txt
SimulatedTrade
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `opportunity` | OneToOne/ForeignKey | Oportunidad ejecutada. |
| `symbol` | CharField | Par. |
| `buy_exchange` | ForeignKey Exchange | Exchange de compra. |
| `sell_exchange` | ForeignKey Exchange | Exchange de venta. |
| `requested_quantity_btc` | DecimalField | Cantidad deseada. |
| `executed_quantity_btc` | DecimalField | Cantidad ejecutada. |
| `buy_price` | DecimalField | Precio de compra. |
| `sell_price` | DecimalField | Precio de venta. |
| `buy_cost` | DecimalField | Costo bruto de compra. |
| `sell_revenue` | DecimalField | Ingreso bruto de venta. |
| `buy_fee` | DecimalField | Fee de compra. |
| `sell_fee` | DecimalField | Fee de venta. |
| `withdrawal_fee` | DecimalField | Fee simulado de retiro. |
| `slippage_cost` | DecimalField | Costo por slippage. |
| `latency_cost` | DecimalField | Costo por latencia. |
| `net_profit` | DecimalField | Resultado neto. |
| `status` | CharField choices | Estado de operación. |
| `failure_reason` | TextField | Motivo si falla. |
| `executed_at` | DateTimeField | Fecha de ejecución. |
| `created_at` | DateTimeField | Creación. |

Estados oficiales:

```txt
executed
partially_executed
failed
discarded
```

---

## 6. Wallet

App:

```txt
wallets
```

Modelo:

```txt
Wallet
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `exchange` | OneToOne Exchange | Exchange asociado. |
| `btc_available` | DecimalField | BTC disponible. |
| `usdt_available` | DecimalField | USDT disponible. |
| `btc_locked` | DecimalField | BTC bloqueado. |
| `usdt_locked` | DecimalField | USDT bloqueado. |
| `total_value_usd` | DecimalField | Valor total estimado. |
| `updated_at` | DateTimeField | Última actualización. |

Regla:

- Toda operación simulada debe actualizar wallets.
- Toda actualización debe registrar movimientos.

---

## 7. WalletMovement

App:

```txt
wallets
```

Modelo:

```txt
WalletMovement
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `wallet` | ForeignKey Wallet | Wallet afectada. |
| `trade` | ForeignKey SimulatedTrade nullable | Trade relacionado. |
| `movement_type` | CharField choices | Tipo de movimiento. |
| `asset` | CharField | BTC o USDT. |
| `amount` | DecimalField | Cantidad movida. |
| `balance_before` | DecimalField | Balance antes. |
| `balance_after` | DecimalField | Balance después. |
| `reference` | CharField | Referencia legible. |
| `created_at` | DateTimeField | Fecha. |

Tipos oficiales:

```txt
buy
sell
fee
lock
release
adjustment
```

---

## 8. SystemLog

App:

```txt
system_logs
```

Modelo:

```txt
SystemLog
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `level` | CharField choices | Nivel del evento. |
| `source` | CharField | Módulo que generó el log. |
| `message` | TextField | Mensaje legible. |
| `metadata` | JSONField | Datos extra. |
| `created_at` | DateTimeField | Fecha. |

Niveles oficiales:

```txt
info
success
warn
error
```

---

## 9. BotSettings

App:

```txt
bot_config
```

Modelo:

```txt
BotSettings
```

Campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | UUID | Identificador. |
| `min_profit_percent` | DecimalField | Umbral mínimo de ganancia. |
| `max_trade_size_btc` | DecimalField | Tamaño máximo por operación. |
| `min_volume_btc` | DecimalField | Volumen mínimo disponible. |
| `slippage_model` | CharField | Modelo de slippage. |
| `max_latency_ms` | PositiveIntegerField | Latencia máxima permitida. |
| `daily_max_loss_usd` | DecimalField | Máxima pérdida diaria. |
| `circuit_breaker_enabled` | BooleanField | Estado circuit breaker. |
| `max_trades_per_minute` | PositiveIntegerField | Límite operativo. |
| `pause_on_feed_disconnect` | BooleanField | Pausa por desconexión. |
| `updated_at` | DateTimeField | Actualización. |

---

## 10. Métricas analytics

Las métricas de rendimiento se calculan desde `ArbitrageOpportunity` y `SimulatedTrade`. No se requiere tabla materializada para el MVP.

Endpoints agregados devuelven:

- P&L acumulado.
- Win rate.
- Ganancia promedio.
- Costo total por fees.
- Oportunidades por estado.
- Ganancia por par de exchanges.

---

## 11. Reglas obligatorias de precisión financiera

- Usar `DecimalField`; no usar `FloatField` para dinero, BTC o porcentajes.
- Guardar precios con precisión suficiente.
- Guardar todos los costos por separado.
- Registrar la razón de decisión en cada oportunidad.
- Registrar logs en cada evento importante.
- Mantener transacciones atómicas al simular trades.

---

## 12. Criterio de aceptación backend

El backend está completo para el MVP cuando existen:

- Modelos migrados.
- Seed data.
- Endpoints REST.
- WebSocket dashboard.
- Motor de detección.
- Simulación de operaciones.
- Actualización de wallets.
- Logs de sistema.
- Settings editables.
