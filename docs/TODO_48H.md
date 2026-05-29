# TODO_48H.md

# Plan oficial de ejecución 48 horas — ArbiBTC

Este documento define el orden de trabajo para construir ArbiBTC sin dispersión. La prioridad es entregar un sistema funcional, desplegado y defendible.

---

## Regla principal

No se avanza a una fase visual secundaria si el dashboard principal, backend, datos y simulación no funcionan.

---

## Hora 0 a 2 — Preparación

### Objetivo

Dejar monorepo y documentación listos.

### Tareas

- Confirmar estructura del monorepo.
- Agregar carpeta `docs/` con los documentos oficiales.
- Crear `.env.example` en backend.
- Crear `.env.example` en frontend.
- Confirmar stack definitivo.
- Crear README inicial.

### Resultado esperado

Repositorio ordenado y listo para desarrollo.

---

## Hora 2 a 6 — Backend base

### Objetivo

Tener Django REST Framework funcionando con Neon.

### Tareas

- Crear proyecto Django.
- Configurar DRF.
- Configurar CORS.
- Configurar conexión PostgreSQL Neon.
- Crear apps oficiales.
- Crear endpoint `/api/health/`.

### Resultado esperado

`GET /api/health/` responde correctamente.

---

## Hora 6 a 10 — Modelos y migraciones

### Objetivo

Crear estructura de datos oficial.

### Tareas

- Implementar `Exchange`.
- Implementar `MarketSnapshot`.
- Implementar `ArbitrageOpportunity`.
- Implementar `SimulatedTrade`.
- Implementar `Wallet`.
- Implementar `WalletMovement`.
- Implementar `SystemLog`.
- Implementar `BotSettings`.
- Ejecutar migraciones.

### Resultado esperado

Base de datos lista con modelos principales.

---

## Hora 10 a 13 — Seed data

### Objetivo

Tener datos realistas para frontend y demo.

### Tareas

- Crear comando `seed_demo`.
- Crear exchanges Binance, Kraken y Coinbase.
- Crear wallets simuladas.
- Crear snapshots de mercado.
- Crear oportunidades.
- Crear trades simulados.
- Crear logs.
- Crear settings iniciales.

### Resultado esperado

Frontend puede consumir datos aunque el motor real aún no esté completo.

---

## Hora 13 a 18 — Endpoints REST

### Objetivo

Exponer contrato API para frontend.

### Tareas

- Crear serializers.
- Crear viewsets o APIViews.
- Exponer endpoints de exchanges.
- Exponer market snapshots.
- Exponer opportunities.
- Exponer trades.
- Exponer wallets.
- Exponer logs.
- Exponer settings.
- Exponer analytics básico.

### Resultado esperado

Frontend tiene datos para todas las pantallas principales.

---

## Hora 18 a 23 — Frontend base

### Objetivo

Tener layout y navegación funcional.

### Tareas

- Crear Vue 3 + TypeScript.
- Configurar Router.
- Configurar Pinia.
- Crear variables CSS.
- Crear global style.
- Crear `AppShell`.
- Crear `AppSidebar`.
- Crear `AppHeader`.
- Crear componentes UI base.
- Crear views vacías.

### Resultado esperado

App navega entre pantallas y respeta paleta visual oficial.

---

## Hora 23 a 28 — Dashboard conectado por REST

### Objetivo

Dashboard funcional con datos reales desde backend.

### Tareas

- Crear services HTTP.
- Crear stores.
- Crear composables base.
- Conectar KPIs.
- Conectar exchange cards.
- Conectar tabla de oportunidades.
- Conectar panel de ejecución.
- Conectar wallets.
- Conectar logs.

### Resultado esperado

Dashboard completo con datos desde API.

---

## Hora 28 a 33 — WebSocket dashboard

### Objetivo

Convertir el dashboard en una vista viva.

### Tareas

- Configurar Django Channels.
- Crear routing WebSocket.
- Crear `DashboardConsumer`.
- Crear eventos oficiales.
- Crear `useDashboardSocket.ts`.
- Actualizar stores por eventos.
- Mostrar estado de conexión en header.

### Resultado esperado

El dashboard recibe eventos en tiempo real.

---

## Hora 33 a 38 — Motor de arbitraje y simulación

### Objetivo

Detectar oportunidades y simular trades.

### Tareas

- Implementar servicio de detección.
- Comparar ask/bid entre exchanges.
- Calcular spread bruto.
- Calcular fees.
- Calcular slippage.
- Calcular penalización por latencia.
- Decidir rentabilidad.
- Crear oportunidad.
- Implementar endpoint simulate.
- Actualizar wallets.
- Registrar wallet movements.
- Registrar logs.
- Emitir eventos WebSocket.

### Resultado esperado

El sistema detecta oportunidades y simula operaciones.

---

## Hora 38 a 42 — Feeds reales de exchanges

### Objetivo

Conectar datos reales de mercado.

### Tareas

- Conectar Binance WebSocket.
- Conectar Kraken WebSocket o REST fallback.
- Normalizar payloads.
- Actualizar snapshots.
- Disparar motor de arbitraje.
- Manejar reconexión.
- Registrar logs técnicos.

### Resultado esperado

El mercado se actualiza desde exchanges reales.

---

## Hora 42 a 45 — Pantallas secundarias

### Objetivo

Completar navegación para demo.

### Tareas

- Oportunidades.
- Operaciones.
- Wallets.
- Rendimiento.
- Logs.
- Configuración.

### Resultado esperado

Todas las rutas muestran información útil.

---

## Hora 45 a 47 — Deploy

### Objetivo

Tener aplicación pública.

### Tareas

- Deploy backend en EC2.
- Configurar Nginx.
- Configurar Neon.
- Ejecutar migraciones.
- Ejecutar seed demo.
- Deploy frontend en Amplify.
- Configurar variables de entorno.
- Probar REST y WebSocket en producción.

### Resultado esperado

URL pública funcionando.

---

## Hora 47 a 48 — Cierre y presentación

### Objetivo

Preparar entrega final.

### Tareas

- Completar README.
- Agregar diagrama de arquitectura.
- Documentar decisiones técnicas.
- Documentar limitaciones.
- Verificar que no hay secretos.
- Probar flujo de demo.
- Revisar UI final.

### Resultado esperado

Entrega lista para jurado.

---

## Prioridad absoluta si el tiempo se reduce

Se entrega únicamente:

- Dashboard.
- Binance + Kraken.
- BTC/USDT.
- Oportunidades detectadas.
- Simulación de trades.
- Wallets actualizadas.
- Logs.
- WebSocket dashboard.
- Deploy público.
- README claro.

---

## Funcionalidades fuera del MVP

No se implementan durante el challenge:

- Login.
- Roles.
- Arbitraje triangular.
- Trading real.
- Más de tres exchanges.
- Microservicios.
- Redis obligatorio.
- Tests extensivos.

Estas funcionalidades se documentan como mejoras futuras.
