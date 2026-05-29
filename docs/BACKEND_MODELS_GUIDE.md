# Especificación de Arquitectura y Modelos de Datos del Backend

Este documento establece la arquitectura técnica, las entidades de dominio y los contratos de API requeridos para el motor de arbitraje **ArbiBTC**. El diseño está orientado a construir un sistema robusto, escalable y auditable.

## 1. Objetivos del Sistema

La arquitectura del backend está diseñada para orquestar las siguientes capacidades principales:
- Establecer y mantener conexiones estables (WebSockets) con exchanges de criptomonedas.
- Estandarizar y agregar datos de mercado (Order Books, Tickers) en tiempo real.
- Identificar y validar oportunidades de arbitraje sensibles a la latencia.
- Computar la rentabilidad neta incorporando costos operativos realistas (comisiones de trading, comisiones de red/retiro, slippage dinámico y penalizaciones por latencia).
- Simular secuencias de ejecución de operaciones (Trades).
- Persistir el estado de las billeteras simuladas (Wallets) y el libro mayor de movimientos (Ledger).
- Exponer el estado del sistema mediante una API RESTful y emitir eventos en tiempo real vía WebSockets.
- Mantener un registro exhaustivo de auditoría técnica y métricas de rendimiento.

## 2. Stack Tecnológico Base

- **Framework:** Django + Django REST Framework (DRF)
- **Capa de Tiempo Real:** Django Channels (WebSockets, ASGI)
- **Base de Datos:** PostgreSQL

## 3. Arquitectura de Aplicaciones

El sistema se divide en los siguientes dominios de negocio discretos:

- `exchanges`: Directorio de exchanges, estructuras de comisiones y estados de conectividad.
- `market_data`: Datos de Nivel 1 (Mejor Bid/Ask) y Nivel 2 (Snapshots de Order Book).
- `opportunities`: Algoritmos de detección de anomalías de spread y decisiones del motor.
- `trades`: Órdenes de ejecución simuladas y sus tramos (compra/venta).
- `wallets`: Saldos simulados y transacciones inmutables.
- `analytics`: Pipelines de agregación para métricas de rendimiento y P&L.
- `system_logs`: Trazabilidad y auditoría a nivel de dominio.
- `bot_config`: Parámetros operativos y límites de riesgo del sistema.

---

## 4. Especificación de Entidades Core (Modelos)

### 4.1 Exchange
Representa un mercado de intercambio conectado al sistema.
- **Atributos:** Nombre, Código Único, Estado de Conexión, URLs (WebSocket/REST), Comisión de Trading (%), Comisión de Retiro, Latencia (ms), Último Timestamp de Conexión.
- **Estados de Conexión:** Online, Offline, Reconnecting, Error.

### 4.2 Par de Trading (Trading Pair)
Define el activo monitoreado por el motor.
- **Atributos:** Activo Base (ej. BTC), Activo Cotizado (ej. USDT), Símbolo, Estado Activo.

### 4.3 Ticker de Mercado (Market Ticker)
Captura la cima del libro de órdenes (datos L1).
- **Atributos:** Mejor Precio/Cantidad de Compra (Bid), Mejor Precio/Cantidad de Venta (Ask), Spread Bruto (%), Volumen 24h, Timestamp.
- *Nota de Implementación:* Se requiere indexación eficiente sobre el timestamp y símbolo para mitigar la degradación de consultas sobre series temporales.

### 4.4 Snapshot del Libro de Órdenes (Order Book)
Captura la profundidad del mercado (datos L2) para validar liquidez y modelar slippage.
- **Atributos:** Matriz de Bids (precio/cantidad), Matriz de Asks (precio/cantidad), Nivel de Profundidad, Timestamp.

---

## 5. Motor de Arbitraje

### 5.1 Oportunidad (Opportunity)
Registra una anomalía de spread detectada y el cómputo de la decisión del sistema.
- **Atributos:** Referencias a Exchanges (Compra/Venta), Par Objetivo, Precios Ask/Bid, Volumen Disponible, Spread Bruto (USD/%), Desglose de Costos (Comisiones, Slippage, Latencia), Beneficio Neto Estimado (USD/%), Score de Liquidez, Razón de la Decisión.
- **Ciclo de Vida (Estados):** Detectada, Rentable, Descartada, Ejecutada, Fallida.

### 5.2 Operación Simulada (Simulated Trade)
Representa el resultado consolidado de la ejecución de un arbitraje.
- **Atributos:** Oportunidad Asociada, Exchanges Involucrados, Cantidad Solicitada/Ejecutada, Precios de Ejecución Ponderados, Beneficio Bruto, Total de Comisiones, Beneficio Neto Consolidado, Mensaje de Resultado.
- **Estados:** Ejecutada, Parcialmente Ejecutada, Fallida, Descartada.

### 5.3 Tramo de Operación (Trade Leg)
Detalla la acción individual (compra o venta) dentro de una operación consolidada.
- **Atributos:** Lado (Buy/Sell), Activo, Cantidad, Precio de Ejecución, Valor Nocional (USD), Comisión Aplicada, Estado de Ejecución.

---

## 6. Libro Mayor Financiero (Wallets)

### 6.1 Billetera (Wallet)
Mantiene el estado consolidado de los activos en un exchange específico.
- **Atributos:** Activo Base Disponible/Bloqueado, Activo Cotizado Disponible/Bloqueado, Valoración Total en USD.

### 6.2 Movimiento de Billetera (Wallet Movement)
Registro inmutable de cualquier mutación de saldo.
- **Atributos:** Tipo de Movimiento (Compra, Venta, Comisión, Bloqueo, Liberación, Ajuste), Activo, Cantidad, Saldo Anterior, Saldo Posterior, Referencia a Operación/Log.

---

## 7. Observabilidad y Rendimiento

### 7.1 Snapshot de Rendimiento (Performance Snapshot)
Métricas agregadas para la visualización del dashboard.
- **Atributos:** P&L Total (USD), Recuento de Operaciones (Total, Rentables, Fallidas), Oportunidades Descartadas, Tasa de Éxito (Win Rate %), Tiempo Promedio de Ejecución, Comisiones Acumuladas.

### 7.2 Log del Sistema (System Log)
Rastro de auditoría técnica.
- **Atributos:** Nivel de Severidad (Info, Warn, Error, Success), Módulo Origen, Mensaje, Contexto JSON.

---

## 8. Configuración del Sistema

### 8.1 Configuración del Motor (Bot Configuration)
Parámetros globales que dictan el comportamiento y gestión de riesgos del algoritmo.
- **Atributos:** Umbral Mínimo de Beneficio (%), Tamaño Máximo de Operación, Volumen Mínimo Requerido, Modelo de Slippage (Fijo vs. Dinámico), Interruptores de Circuito (Circuit Breakers), Límite Máximo de Pérdida Diaria.

---

## 9. Contratos de API REST y Eventos de Tiempo Real

### 9.1 Documentación Interactiva (Swagger / OpenAPI)
- **Esquema OpenAPI:** `/api/schema/`
- **Swagger UI:** `/api/docs/swagger/`
- **Redoc UI:** `/api/docs/redoc/`

### 9.2 Endpoints REST Principales
- **Mercados:** `/api/markets/tickers/`, `/api/exchanges/`
- **Oportunidades:** `/api/opportunities/`, `/api/opportunities/summary/`, `/api/opportunities/{id}/simulate/`
- **Operaciones:** `/api/trades/`, `/api/trades/summary/`
- **Finanzas:** `/api/wallets/`, `/api/wallets/summary/`, `/api/wallet-movements/`
- **Rendimiento:** `/api/analytics/pnl/`, `/api/analytics/summary/`
- **Plano de Control:** `/api/bot-config/active/`, `/api/bot-control/start/`, `/api/bot-control/pause/`
- **Auditoría:** `/api/logs/`

### 9.2 Payloads de WebSockets (Django Channels)
El flujo de datos en vivo debe canalizarse preferiblemente mediante una única conexión multiplexada (ej. `/ws/dashboard/`) para emitir los siguientes eventos:
- `market.ticker.updated`
- `opportunity.detected`
- `trade.executed`
- `wallet.updated`
- `system.log.created`

---

## 10. Restricciones y Reglas de Negocio Centrales

### 10.1 Cálculo de Rentabilidad Neta Estricto
Cualquier oportunidad debe computarse bajo la siguiente fórmula de rentabilidad neta antes de autorizar su ejecución:
`Beneficio Neto = (Precio Bid * Cantidad) - (Precio Ask * Cantidad) - Suma(Comisiones Trading) - Comisión Retiro - Costo por Slippage - Penalización por Latencia`

### 10.2 Criterios de Autorización de Ejecución
Una operación simulada está estrictamente autorizada solo si se cumplen simultáneamente todas las siguientes precondiciones:
1. `Beneficio Neto Estimado (%) >= Umbral Mínimo Configurado`
2. `Volumen Disponible L2 >= Volumen Mínimo Requerido`
3. `Latencia <= Latencia Máxima Permitida`
4. Los saldos de las billeteras satisfacen la liquidez requerida para ambas transacciones (incluyendo comisiones).
5. Los mecanismos de gestión de riesgo (Circuit Breakers) permanecen inactivos.

### 10.3 Ejecución Parcial
En escenarios donde la liquidez del Order Book sea inferior al tamaño máximo de operación configurado, el motor debe degradar elegantemente a una ejecución parcial, recalculando los costos y ajustando el volumen a:
`Cantidad a Ejecutar = MIN(Tamaño Máximo Configurado, Volumen Disponible, Límite de Billetera)`

### 10.4 Razonamiento del Sistema
El sistema debe poseer un alto grado de explicabilidad. Toda oportunidad detectada que concluya su ciclo de vida (ya sea en descarte o ejecución) debe persistir de manera obligatoria la razón algorítmica de la decisión, proporcionando transparencia para la trazabilidad y auditoría operativa.
