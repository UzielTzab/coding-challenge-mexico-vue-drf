# ARCHITECTURE.md

# Arquitectura oficial — ArbiBTC

Este documento define la arquitectura que se implementará y respetará durante el desarrollo del sistema **ArbiBTC**, una plataforma web para detección y simulación de oportunidades de arbitraje de Bitcoin en tiempo real.

El proyecto se desarrolla bajo una monorepo con frontend en Vue 3, backend en Django REST Framework, comunicación en tiempo real mediante WebSockets, base de datos PostgreSQL en Neon y despliegue en AWS.

---

## 1. Estructura oficial del monorepo

```txt
CODING_CHALLENGE_MEXICO/
├── backend/
├── docs/
├── frontend/
├── .gitignore
├── amplify.yml
└── README.md
```

La carpeta `docs/` contiene la arquitectura, contrato API, eventos WebSocket, guía UI, modelos backend, despliegue y plan de ejecución.

---

## 2. Stack oficial

### Frontend

- Vue 3.
- TypeScript.
- Vite.
- Pinia.
- Vue Router.
- Axios para REST API.
- WebSocket nativo encapsulado en composables.
- CSS global con variables.
- Recharts, ECharts o Chart.js para visualización financiera.

### Backend

- Python.
- Django.
- Django REST Framework.
- Django Channels.
- ASGI.
- PostgreSQL en Neon.
- Uvicorn o Daphne para ASGI.
- Gunicorn para procesos HTTP si se separa el deployment.

### Infraestructura

- Frontend en AWS Amplify.
- Backend en AWS EC2.
- Base de datos en Neon PostgreSQL.
- Nginx como reverse proxy.
- Variables de entorno para configuración sensible.

---

## 3. Objetivo del sistema

ArbiBTC monitorea precios de BTC en múltiples exchanges, detecta divergencias entre el mejor precio de compra y el mejor precio de venta, calcula rentabilidad neta considerando costos reales y simula operaciones de arbitraje actualizando wallets, historial y métricas de rendimiento.

El sistema no ejecuta operaciones reales. Toda ejecución es simulada.

---

## 4. Flujo general de datos

```txt
Exchange WebSocket Feeds
        ↓
Market Data Ingestion Service
        ↓
Market Snapshot Normalizer
        ↓
Arbitrage Engine
        ↓
Risk & Profitability Evaluator
        ↓
Simulation Engine
        ↓
Wallet Service / Trade Service / Logs
        ↓
PostgreSQL Neon
        ↓
Django REST API + Django Channels
        ↓
Vue 3 Dashboard
```

---

## 5. Arquitectura backend

El backend se divide por dominios. Cada dominio mantiene sus modelos, serializers, servicios, consumers, tasks y tests.

```txt
backend/
backend/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── routing.py
│   ├── celery.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── production.py
│       └── testing.py
│
├── apps/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── exceptions.py
│   │   ├── permissions.py
│   │   ├── pagination.py
│   │   ├── responses.py
│   │   ├── throttling.py
│   │   ├── validators.py
│   │   ├── constants.py
│   │   ├── health.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_health.py
│   │
│   ├── exchanges/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── repositories.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── clients/
│   │   │   ├── __init__.py
│   │   │   ├── base_client.py
│   │   │   ├── binance_client.py
│   │   │   ├── kraken_client.py
│   │   │   ├── coinbase_client.py
│   │   │   └── okx_client.py
│   │   ├── normalizers/
│   │   │   ├── __init__.py
│   │   │   ├── base_normalizer.py
│   │   │   ├── binance_normalizer.py
│   │   │   ├── kraken_normalizer.py
│   │   │   ├── coinbase_normalizer.py
│   │   │   └── okx_normalizer.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── seed_exchanges.py
│   │   │       └── test_exchange_feeds.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_clients.py
│   │       └── test_normalizers.py
│   │
│   ├── market_data/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── repositories.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── tasks.py
│   │   ├── consumers.py
│   │   ├── routing.py
│   │   ├── schemas.py
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── ticker_processor.py
│   │   │   ├── order_book_processor.py
│   │   │   └── latency_processor.py
│   │   ├── streams/
│   │   │   ├── __init__.py
│   │   │   ├── stream_manager.py
│   │   │   ├── binance_stream.py
│   │   │   ├── kraken_stream.py
│   │   │   ├── coinbase_stream.py
│   │   │   └── reconnect_policy.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── run_market_streams.py
│   │   │       ├── seed_market_snapshots.py
│   │   │       └── clean_market_snapshots.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_processors.py
│   │       ├── test_streams.py
│   │       └── test_api.py
│   │
│   ├── arbitrage/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── repositories.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── tasks.py
│   │   ├── consumers.py
│   │   ├── routing.py
│   │   ├── schemas.py
│   │   ├── engine/
│   │   │   ├── __init__.py
│   │   │   ├── arbitrage_engine.py
│   │   │   ├── opportunity_detector.py
│   │   │   ├── profitability_calculator.py
│   │   │   ├── liquidity_checker.py
│   │   │   ├── risk_checker.py
│   │   │   ├── opportunity_ranker.py
│   │   │   └── decision_engine.py
│   │   ├── calculators/
│   │   │   ├── __init__.py
│   │   │   ├── fee_calculator.py
│   │   │   ├── slippage_calculator.py
│   │   │   ├── spread_calculator.py
│   │   │   ├── latency_penalty_calculator.py
│   │   │   └── net_profit_calculator.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── run_arbitrage_engine.py
│   │   │       ├── detect_arbitrage_once.py
│   │   │       └── seed_opportunities.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_calculators.py
│   │       ├── test_engine.py
│   │       └── test_api.py
│   │
│   ├── trading/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── repositories.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── tasks.py
│   │   ├── schemas.py
│   │   ├── simulation/
│   │   │   ├── __init__.py
│   │   │   ├── simulation_engine.py
│   │   │   ├── trade_executor.py
│   │   │   ├── partial_fill_handler.py
│   │   │   ├── balance_updater.py
│   │   │   ├── execution_result_builder.py
│   │   │   └── trade_validator.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── simulate_trade.py
│   │   │       └── seed_trades.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_simulation_engine.py
│   │       ├── test_partial_fills.py
│   │       └── test_api.py
│   │
│   ├── wallets/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── repositories.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── tasks.py
│   │   ├── ledger/
│   │   │   ├── __init__.py
│   │   │   ├── wallet_ledger.py
│   │   │   ├── movement_factory.py
│   │   │   ├── balance_calculator.py
│   │   │   └── balance_validator.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── seed_wallets.py
│   │   │       └── recalculate_wallets.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_ledger.py
│   │       └── test_api.py
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── repositories.py
│   │   ├── constants.py
│   │   ├── calculators/
│   │   │   ├── __init__.py
│   │   │   ├── pnl_calculator.py
│   │   │   ├── win_rate_calculator.py
│   │   │   ├── opportunity_stats_calculator.py
│   │   │   ├── exchange_pair_profit_calculator.py
│   │   │   └── execution_time_calculator.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_calculators.py
│   │       └── test_api.py
│   │
│   ├── system_logs/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── repositories.py
│   │   ├── constants.py
│   │   ├── consumers.py
│   │   ├── routing.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_logs.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       └── test_api.py
│   │
│   ├── bot_control/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── state/
│   │   │   ├── __init__.py
│   │   │   ├── bot_state_machine.py
│   │   │   ├── bot_status.py
│   │   │   └── circuit_breaker.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── reset_bot_state.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_state_machine.py
│   │       └── test_api.py
│   │
│   └── settings_app/
│       ├── __init__.py
│       ├── apps.py
│       ├── admin.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── services.py
│       ├── selectors.py
│       ├── constants.py
│       ├── validators.py
│       ├── management/
│       │   └── commands/
│       │       └── seed_default_settings.py
│       └── tests/
│           ├── __init__.py
│           ├── test_models.py
│           └── test_api.py
│
├── common/
│   ├── __init__.py
│   ├── env.py
│   ├── time.py
│   ├── money.py
│   ├── decimals.py
│   ├── enums.py
│   ├── logging.py
│   ├── websocket.py
│   ├── async_utils.py
│   ├── database.py
│   └── typing.py
│
├── scripts/
│   ├── start_dev.sh
│   ├── run_migrations.sh
│   ├── seed_demo.sh
│   ├── run_streams.sh
│   ├── run_engine.sh
│   ├── collectstatic.sh
│   └── deploy_ec2.sh
│
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
│
├── static/
│   └── .gitkeep
│
├── media/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
├── templates/
│   └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── factories.py
│   └── integration/
│       ├── __init__.py
│       ├── test_arbitrage_flow.py
│       ├── test_trade_simulation_flow.py
│       └── test_dashboard_api_flow.py
│
├── .env.example
├── .env.development
├── .env.production.example
├── manage.py
├── pytest.ini
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── gunicorn.conf.py
└── README.md
```

### Responsabilidad por app

| App | Responsabilidad |
|---|---|
| `exchanges` | Catálogo y configuración de exchanges. |
| `market_data` | Captura y normalización de precios bid/ask. |
| `arbitrage` | Detección y evaluación de oportunidades. |
| `trading` | Simulación de operaciones. |
| `wallets` | Saldos simulados y movimientos. |
| `analytics` | Métricas agregadas y rendimiento. |
| `system_logs` | Registro de eventos técnicos y decisiones del bot. |
| `bot_config` | Parámetros editables de estrategia, fees y riesgo. |

---

## 6. Arquitectura frontend

El frontend se divide por responsabilidades visuales, estado, comunicación HTTP, WebSockets y lógica reusable.

```txt
frontend/
├── public/
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   ├── assets/
│   │   ├── icons/
│   │   │   ├── bitcoin.svg
│   │   │   ├── binance.svg
│   │   │   ├── coinbase.svg
│   │   │   ├── kraken.svg
│   │   │   ├── dashboard.svg
│   │   │   ├── markets.svg
│   │   │   ├── opportunities.svg
│   │   │   ├── operations.svg
│   │   │   ├── wallets.svg
│   │   │   ├── performance.svg
│   │   │   ├── logs.svg
│   │   │   └── settings.svg
│   │   │
│   │   ├── images/
│   │   │   ├── empty-state.svg
│   │   │   └── error-state.svg
│   │   │
│   │   └── logos/
│   │       ├── arbi-btc-logo.svg
│   │       └── arbi-btc-symbol.svg
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppShell.vue
│   │   │   ├── AppSidebar.vue
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppContent.vue
│   │   │   ├── AppPageHeader.vue
│   │   │   └── AppMobileSidebar.vue
│   │   │
│   │   ├── ui/
│   │   │   ├── AppButton.vue
│   │   │   ├── AppCard.vue
│   │   │   ├── AppBadge.vue
│   │   │   ├── AppTable.vue
│   │   │   ├── AppInput.vue
│   │   │   ├── AppSelect.vue
│   │   │   ├── AppModal.vue
│   │   │   ├── AppDrawer.vue
│   │   │   ├── AppTabs.vue
│   │   │   ├── AppTooltip.vue
│   │   │   ├── AppSpinner.vue
│   │   │   ├── AppSkeleton.vue
│   │   │   ├── AppEmptyState.vue
│   │   │   ├── AppErrorState.vue
│   │   │   ├── AppStatCard.vue
│   │   │   ├── AppStatusDot.vue
│   │   │   ├── AppMetricDelta.vue
│   │   │   ├── AppSearchInput.vue
│   │   │   ├── AppDateRangePicker.vue
│   │   │   └── AppPagination.vue
│   │   │
│   │   ├── dashboard/
│   │   │   ├── DashboardKpiGrid.vue
│   │   │   ├── DashboardStatusBar.vue
│   │   │   ├── KpiCard.vue
│   │   │   ├── ExchangeGrid.vue
│   │   │   ├── ExchangeCard.vue
│   │   │   ├── MiniOrderBook.vue
│   │   │   ├── OpportunityTable.vue
│   │   │   ├── ExecutionPanel.vue
│   │   │   ├── ExecutionFlow.vue
│   │   │   ├── ExecutionCostBreakdown.vue
│   │   │   ├── WalletSummary.vue
│   │   │   ├── PerformanceSummary.vue
│   │   │   ├── SystemLogPanel.vue
│   │   │   └── BotControlPanel.vue
│   │   │
│   │   ├── markets/
│   │   │   ├── MarketFilters.vue
│   │   │   ├── MarketTable.vue
│   │   │   ├── MarketExchangeCard.vue
│   │   │   ├── ExchangeStatusGrid.vue
│   │   │   ├── ExchangeStatusCard.vue
│   │   │   ├── OrderBookDepth.vue
│   │   │   ├── OrderBookTable.vue
│   │   │   ├── MarketSpreadChart.vue
│   │   │   └── MarketLatencyCard.vue
│   │   │
│   │   ├── opportunities/
│   │   │   ├── OpportunitySummaryCards.vue
│   │   │   ├── OpportunityFilters.vue
│   │   │   ├── OpportunityListTable.vue
│   │   │   ├── OpportunityStatusBadge.vue
│   │   │   ├── OpportunityProfitCell.vue
│   │   │   ├── OpportunityDetailDrawer.vue
│   │   │   ├── OpportunityCalculationBreakdown.vue
│   │   │   ├── OpportunityDecisionPanel.vue
│   │   │   ├── OpportunityLiquidityPanel.vue
│   │   │   └── OpportunityExecuteButton.vue
│   │   │
│   │   ├── operations/
│   │   │   ├── OperationSummaryCards.vue
│   │   │   ├── OperationFilters.vue
│   │   │   ├── OperationHistoryTable.vue
│   │   │   ├── OperationStatusBadge.vue
│   │   │   ├── OperationDetailDrawer.vue
│   │   │   ├── OperationLegsPanel.vue
│   │   │   ├── OperationBalancesPanel.vue
│   │   │   ├── OperationCostBreakdown.vue
│   │   │   └── OperationResultPanel.vue
│   │   │
│   │   ├── wallets/
│   │   │   ├── WalletSummaryCards.vue
│   │   │   ├── WalletGrid.vue
│   │   │   ├── WalletCard.vue
│   │   │   ├── WalletBalanceTable.vue
│   │   │   ├── WalletMovementTable.vue
│   │   │   ├── WalletMovementFilters.vue
│   │   │   ├── WalletAssetBadge.vue
│   │   │   └── WalletTotalValueCard.vue
│   │   │
│   │   ├── performance/
│   │   │   ├── PerformanceKpiGrid.vue
│   │   │   ├── PnlLineChart.vue
│   │   │   ├── ProfitByExchangeChart.vue
│   │   │   ├── OpportunityStatusDonut.vue
│   │   │   ├── OpportunitiesPerHourChart.vue
│   │   │   ├── FeesCostChart.vue
│   │   │   ├── WinRateCard.vue
│   │   │   ├── AverageExecutionTimeCard.vue
│   │   │   └── PerformancePeriodFilters.vue
│   │   │
│   │   ├── logs/
│   │   │   ├── LogFilters.vue
│   │   │   ├── LogTerminal.vue
│   │   │   ├── LogLevelBadge.vue
│   │   │   ├── LogRow.vue
│   │   │   ├── ServiceStatusGrid.vue
│   │   │   ├── ServiceStatusCard.vue
│   │   │   └── AutoScrollToggle.vue
│   │   │
│   │   └── settings/
│   │       ├── StrategySettingsForm.vue
│   │       ├── RiskSettingsForm.vue
│   │       ├── FeeSettingsTable.vue
│   │       ├── ExchangeSettingsTable.vue
│   │       ├── SimulationSettingsForm.vue
│   │       ├── SettingsSection.vue
│   │       ├── SettingsActions.vue
│   │       └── CircuitBreakerCard.vue
│   │
│   ├── composables/
│   │   ├── useApi.ts
│   │   ├── useWebSocket.ts
│   │   ├── useDashboardSocket.ts
│   │   ├── useMarketSocket.ts
│   │   ├── useOpportunitiesSocket.ts
│   │   ├── useBotState.ts
│   │   ├── useMarketData.ts
│   │   ├── useOpportunities.ts
│   │   ├── useTrades.ts
│   │   ├── useWallets.ts
│   │   ├── useLogs.ts
│   │   ├── useSettings.ts
│   │   ├── useAnalytics.ts
│   │   ├── useFilters.ts
│   │   ├── usePagination.ts
│   │   ├── useSorting.ts
│   │   ├── useFormatters.ts
│   │   ├── useCurrencyFormatter.ts
│   │   ├── usePercentFormatter.ts
│   │   ├── useDateFormatter.ts
│   │   ├── useToast.ts
│   │   ├── useModal.ts
│   │   └── useLocalStorage.ts
│   │
│   ├── services/
│   │   ├── api.client.ts
│   │   ├── websocket.client.ts
│   │   ├── dashboard.service.ts
│   │   ├── market.service.ts
│   │   ├── opportunities.service.ts
│   │   ├── trades.service.ts
│   │   ├── wallets.service.ts
│   │   ├── analytics.service.ts
│   │   ├── logs.service.ts
│   │   ├── settings.service.ts
│   │   ├── bot.service.ts
│   │   └── health.service.ts
│   │
│   ├── stores/
│   │   ├── dashboard.store.ts
│   │   ├── market.store.ts
│   │   ├── opportunities.store.ts
│   │   ├── trades.store.ts
│   │   ├── wallets.store.ts
│   │   ├── analytics.store.ts
│   │   ├── logs.store.ts
│   │   ├── settings.store.ts
│   │   ├── bot.store.ts
│   │   └── ui.store.ts
│   │
│   ├── router/
│   │   ├── index.ts
│   │   ├── routes.ts
│   │   └── guards.ts
│   │
│   ├── styles/
│   │   ├── variables.css
│   │   ├── globals.css
│   │   ├── typography.css
│   │   ├── layout.css
│   │   ├── utilities.css
│   │   ├── tables.css
│   │   ├── forms.css
│   │   ├── charts.css
│   │   └── animations.css
│   │
│   ├── types/
│   │   ├── api.types.ts
│   │   ├── websocket.types.ts
│   │   ├── domain.types.ts
│   │   ├── dashboard.types.ts
│   │   ├── market.types.ts
│   │   ├── opportunity.types.ts
│   │   ├── trade.types.ts
│   │   ├── wallet.types.ts
│   │   ├── analytics.types.ts
│   │   ├── log.types.ts
│   │   ├── settings.types.ts
│   │   └── ui.types.ts
│   │
│   ├── utils/
│   │   ├── constants.ts
│   │   ├── env.ts
│   │   ├── routes.ts
│   │   ├── formatCurrency.ts
│   │   ├── formatPercent.ts
│   │   ├── formatDate.ts
│   │   ├── formatExchange.ts
│   │   ├── calculateSpread.ts
│   │   ├── calculateProfit.ts
│   │   ├── mapStatusColor.ts
│   │   ├── mapLogLevelColor.ts
│   │   ├── validators.ts
│   │   └── sleep.ts
│   │
│   ├── views/
│   │   ├── DashboardView.vue
│   │   ├── MarketsView.vue
│   │   ├── OpportunitiesView.vue
│   │   ├── OperationsView.vue
│   │   ├── WalletsView.vue
│   │   ├── PerformanceView.vue
│   │   ├── LogsView.vue
│   │   ├── SettingsView.vue
│   │   └── NotFoundView.vue
│   │
│   ├── config/
│   │   ├── app.config.ts
│   │   ├── api.config.ts
│   │   ├── websocket.config.ts
│   │   ├── chart.config.ts
│   │   └── theme.config.ts
│   │
│   ├── mocks/
│   │   ├── dashboard.mock.ts
│   │   ├── market.mock.ts
│   │   ├── opportunities.mock.ts
│   │   ├── trades.mock.ts
│   │   ├── wallets.mock.ts
│   │   ├── analytics.mock.ts
│   │   ├── logs.mock.ts
│   │   └── settings.mock.ts
│   │
│   ├── App.vue
│   ├── main.ts
│   └── vite-env.d.ts
│
├── .env.example
├── .env.development
├── .env.production
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
├── eslint.config.js
├── prettier.config.js
└── README.md
```

### Responsabilidad por carpeta

| Carpeta | Responsabilidad |
|---|---|
| `components/layout` | Estructura global: sidebar, header, shell. |
| `components/ui` | Componentes reutilizables base. |
| `components/dashboard` | Widgets específicos del dashboard. |
| `composables` | Lógica reusable: WebSockets, fetch, formato, timers. |
| `services` | Cliente REST y módulos por recurso. |
| `stores` | Estado global con Pinia. |
| `types` | Interfaces TypeScript oficiales. |
| `views` | Pantallas completas. |
| `styles` | Variables y estilos globales. |

---

## 7. Comunicación REST y WebSocket

El sistema usa REST para consultas históricas, filtros, resúmenes y configuración. WebSocket se usa para datos vivos y eventos del bot.

### REST

REST entrega:

- Listados paginados.
- Resúmenes de pantalla.
- Detalles de registros.
- Configuración.
- Historial.

### WebSocket

WebSocket entrega:

- Actualización de mercado.
- Oportunidad detectada.
- Trade simulado.
- Wallet actualizada.
- Log del sistema.
- Estado del bot.

---

## 8. Exchanges iniciales

El sistema implementa inicialmente:

1. Binance.
2. Kraken.
3. Coinbase como tercer exchange si el tiempo lo permite.

El par principal del challenge será:

```txt
BTC/USDT
```

Si un exchange usa `BTC/USD`, el backend normaliza el símbolo para visualización y cálculo.

---

## 9. Reglas principales del motor de arbitraje

Una oportunidad existe cuando:

```txt
ask_price_exchange_a < bid_price_exchange_b
```

La oportunidad solo se marca como rentable cuando:

```txt
net_profit > 0
net_profit_percent >= min_profit_threshold
available_volume > 0
wallet_balance_is_sufficient = true
market_data_is_fresh = true
```

La fórmula base es:

```txt
buy_cost = ask_price * quantity
sell_revenue = bid_price * quantity
buy_fee = buy_cost * buy_fee_percent
sell_fee = sell_revenue * sell_fee_percent
net_profit = sell_revenue - buy_cost - buy_fee - sell_fee - slippage_cost - withdrawal_fee - latency_penalty
```

---

## 10. Prioridad funcional

El desarrollo se ejecuta en este orden:

1. Backend base con modelos y endpoints.
2. Seed data realista.
3. Frontend base con layout, estilos y navegación.
4. Dashboard conectado a API.
5. WebSocket interno dashboard.
6. Motor básico de arbitraje.
7. Simulación de operaciones.
8. Wallet movements y logs.
9. Conexión a exchanges reales.
10. Pantallas secundarias.
11. Deploy.
12. README y demo.

---

## 11. Restricciones de alcance

No se implementa login en la primera entrega.

No se ejecutan trades reales.

No se implementa arbitraje triangular en la primera entrega.

No se integran más de tres exchanges durante el challenge.

No se guardan credenciales de trading porque solo se usan APIs públicas de mercado.

---

## 12. Criterio de aceptación

La arquitectura se considera cumplida cuando:

- El backend expone REST API y WebSocket.
- El dashboard muestra datos vivos.
- El sistema detecta oportunidades.
- El sistema simula operaciones.
- Las wallets se actualizan.
- Los logs explican las decisiones del bot.
- La app está desplegada públicamente.
- El README documenta decisiones técnicas y ejecución local.
