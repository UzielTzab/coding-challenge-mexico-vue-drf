# FRONTEND_UI_GUIDE.md — ArbiBTC

Guía de diseño e implementación frontend para la web app **ArbiBTC**, un dashboard de arbitraje de Bitcoin en modo simulación.

Este documento debe ser usado por el equipo frontend para mantener una interfaz consistente, limpia, escalable y alineada con los requerimientos técnicos y de negocio.

---

## 1. Objetivo visual de la web

La aplicación debe sentirse como una plataforma **fintech profesional**, enfocada en trading, monitoreo en tiempo real y simulación de operaciones.

La interfaz debe comunicar:

- Velocidad.
- Precisión.
- Sistema en vivo.
- Control de riesgo.
- Datos financieros en tiempo real.
- Robustez técnica.

El diseño debe ser **dark mode por defecto**.

---

## 2. Stack frontend

Stack tecnológico base:

```txt
Vue 3
Vite
TypeScript
Pinia
Vue Router
Axios
WebSocket nativo o composable custom
Chart.js / ECharts / ApexCharts
CSS global + variables CSS
```

---

## 3. Paleta de colores oficial

### Colores principales

```css
:root {
  --color-bg-dashboard: #0C0E1F;
  --color-bg-sidebar: #14172A;

  --color-primary-light: #7EB0F3;
  --color-primary-strong: #4451BB;

  --color-success: #03B987;
  --color-danger: #FA6C6E;

  --color-warning: #F4B740;
  --color-info: #7EB0F3;
}
```

### Colores complementarios

```css
:root {
  --color-bg-card: #111529;
  --color-bg-card-soft: #171B33;
  --color-bg-terminal: #070A16;

  --color-border: rgba(255, 255, 255, 0.08);
  --color-border-strong: rgba(255, 255, 255, 0.14);

  --color-text-primary: #FFFFFF;
  --color-text-secondary: #A8B0C3;
  --color-text-muted: #6F7890;

  --color-shadow-primary: rgba(68, 81, 187, 0.35);
  --color-shadow-success: rgba(3, 185, 135, 0.35);
  --color-shadow-danger: rgba(250, 108, 110, 0.30);
}
```

### Gradiente principal

Este gradiente debe usarse en:

- Botón principal.
- Opción activa del sidebar.
- Elementos seleccionados.
- CTAs importantes.

```css
:root {
  --gradient-primary: linear-gradient(180deg, #7EB0F3 0%, #4451BB 100%);
}
```

---

## 4. Tipografía global

Tipografía principal:

```txt
Inter
```

Tipografía de respaldo (fallback):

```txt
Manrope
```

Tipografía para datos financieros:

```txt
JetBrains Mono
```

Respaldo:

```txt
IBM Plex Mono
```

### Configuración de importación

En `index.html` o en el CSS global:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Variables tipográficas

```css
:root {
  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;

  --text-xs: 0.75rem;   /* 12px */
  --text-sm: 0.875rem;  /* 14px */
  --text-md: 1rem;      /* 16px */
  --text-lg: 1.125rem;  /* 18px */
  --text-xl: 1.5rem;    /* 24px */
  --text-2xl: 2rem;     /* 32px */
}
```

### Jerarquía tipográfica

```css
h1 {
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-text-primary);
}

h2 {
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text-primary);
}

p,
span,
button,
input,
select,
table {
  font-family: var(--font-sans);
}

.numeric,
.money,
.percentage,
.timestamp {
  font-family: var(--font-mono);
}
```

---

## 5. Estilos globales base

Crear un archivo:

```txt
src/styles/global.css
```

Contenido requerido:

```css
* {
  box-sizing: border-box;
}

html,
body,
#app {
  width: 100%;
  min-height: 100%;
  margin: 0;
}

body {
  font-family: var(--font-sans);
  background: var(--color-bg-dashboard);
  color: var(--color-text-primary);
  overflow-x: hidden;
}

button,
input,
textarea,
select {
  font: inherit;
}

button {
  border: none;
  cursor: pointer;
}

a {
  color: inherit;
  text-decoration: none;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #0A0D1A;
}

::-webkit-scrollbar-thumb {
  background: #2A3154;
  border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
  background: #3A4370;
}
```

---

## 6. Layout global obligatorio

Todas las pantallas deben vivir dentro de un layout principal.

```txt
AppShell
├── AppSidebar
├── MainArea
│   ├── AppHeader
│   └── RouterView
```

### Dimensiones base

```css
:root {
  --sidebar-width: 260px;
  --header-height: 72px;
  --content-padding: 24px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
}
```

### AppShell

```css
.app-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: var(--sidebar-width) 1fr;
  background: var(--color-bg-dashboard);
}

.app-main {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.app-content {
  padding: var(--content-padding);
}
```

---

## 7. Sidebar obligatorio

Componente:

```txt
src/components/layout/AppSidebar.vue
```

### Color

```css
background: var(--color-bg-sidebar);
```

### Contenido

Debe incluir:

```txt
Logo: ArbiBTC
Subtexto: Bitcoin Arbitrage Bot

Dashboard
Mercados
Oportunidades
Operaciones
Wallets
Rendimiento
Logs
Configuración

Modo: Simulación
Estado del bot
Versión: ArbiBTC v1.0.0
```

### Item activo

```css
.sidebar-link--active {
  background: var(--gradient-primary);
  color: #FFFFFF;
  box-shadow: 0 8px 20px var(--color-shadow-primary);
}
```

### Item normal

```css
.sidebar-link {
  height: 44px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  transition: 160ms ease;
}

.sidebar-link:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary);
}
```

---

## 8. Header obligatorio

Componente:

```txt
src/components/layout/AppHeader.vue
```

### Debe mostrar

```txt
Título de la pantalla
Subtítulo de la pantalla
Backend: En línea
WebSockets: En línea
Motor Bot: Activo
DB: Conectada
Latencia: 28 ms
Hora UTC
Botón Iniciar Bot
Botón Pausar
```

### Estilo

```css
.app-header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--content-padding);
  background: var(--color-bg-dashboard);
  border-bottom: 1px solid var(--color-border);
}
```

---

## 9. Componentes obligatorios UI

Estos componentes deben existir sí o sí para evitar repetir estilos.

```txt
src/components/ui/AppButton.vue
src/components/ui/AppCard.vue
src/components/ui/AppBadge.vue
src/components/ui/AppTable.vue
src/components/ui/AppInput.vue
src/components/ui/AppSelect.vue
src/components/ui/AppTabs.vue
src/components/ui/AppModal.vue
src/components/ui/AppEmptyState.vue
src/components/ui/AppLoadingState.vue
src/components/ui/AppErrorState.vue
```

---

## 10. AppButton

Componente obligatorio:

```txt
AppButton.vue
```

### Variantes

```txt
primary
secondary
danger
ghost
```

### Primary

Uso:

- Iniciar Bot.
- Ejecutar simulación.
- Guardar configuración.

```css
.btn--primary {
  background: var(--gradient-primary);
  color: #FFFFFF;
  box-shadow: 0 8px 20px var(--color-shadow-primary);
}
```

### Secondary

```css
.btn--secondary {
  background: var(--color-bg-card-soft);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}
```

### Danger

```css
.btn--danger {
  background: rgba(250, 108, 110, 0.14);
  color: var(--color-danger);
  border: 1px solid rgba(250, 108, 110, 0.35);
}
```

### Base

```css
.btn {
  min-height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 16px;
  border-radius: var(--radius-md);
  font-weight: 600;
  transition: 160ms ease;
}

.btn:hover {
  transform: translateY(-1px);
}
```

---

## 11. AppCard

Componente obligatorio:

```txt
AppCard.vue
```

Uso para cualquier bloque visual.

```css
.app-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px;
}
```

Variantes:

```txt
default
soft
highlighted
terminal
```

```css
.app-card--soft {
  background: var(--color-bg-card-soft);
}

.app-card--highlighted {
  border-color: rgba(126, 176, 243, 0.65);
  box-shadow: 0 0 24px rgba(68, 81, 187, 0.25);
}

.app-card--terminal {
  background: var(--color-bg-terminal);
  font-family: var(--font-mono);
}
```

---

## 12. AppBadge

Componente obligatorio:

```txt
AppBadge.vue
```

Estados:

```txt
success
error
warning
info
neutral
```

Uso para:

- En línea.
- Activo.
- Rentable.
- Descartada.
- Ejecutada.
- Fallida.
- Pausado.

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: var(--text-xs);
  font-weight: 600;
}

.badge--success {
  background: rgba(3, 185, 135, 0.12);
  color: var(--color-success);
  border: 1px solid rgba(3, 185, 135, 0.30);
}

.badge--error {
  background: rgba(250, 108, 110, 0.12);
  color: var(--color-danger);
  border: 1px solid rgba(250, 108, 110, 0.30);
}

.badge--warning {
  background: rgba(244, 183, 64, 0.12);
  color: var(--color-warning);
  border: 1px solid rgba(244, 183, 64, 0.30);
}

.badge--info {
  background: rgba(126, 176, 243, 0.12);
  color: var(--color-primary-light);
  border: 1px solid rgba(126, 176, 243, 0.30);
}
```

---

## 13. Componentes específicos del dashboard

Estos componentes deben existir para la pantalla principal.

```txt
src/components/dashboard/KpiCard.vue
src/components/dashboard/ExchangeCard.vue
src/components/dashboard/OpportunityTable.vue
src/components/dashboard/ExecutionPanel.vue
src/components/dashboard/WalletSummary.vue
src/components/dashboard/PerformanceCharts.vue
src/components/dashboard/SystemLogPanel.vue
```

---

## 14. KpiCard

Debe mostrar:

```txt
Título
Valor principal
Variación
Mini gráfico opcional
```

Ejemplo:

```txt
P&L acumulado
$1,246.38
▲ 18.7% vs 1h
```

Colores:

```txt
Positivo: #03B987
Negativo: #FA6C6E
Neutro: #A8B0C3
```

---

## 15. ExchangeCard

Debe mostrar datos del exchange.

Campos obligatorios:

```txt
Nombre del exchange
Estado de conexión
Best Bid
Best Ask
Spread
Volumen 24h
Última actualización
Mini order book
```

Bids:

```css
color: var(--color-success);
```

Asks:

```css
color: var(--color-danger);
```

Barras del order book:

```css
.orderbook-bar--bid {
  background: rgba(3, 185, 135, 0.75);
}

.orderbook-bar--ask {
  background: rgba(250, 108, 110, 0.75);
}
```

---

## 16. OpportunityTable

Tabla principal de oportunidades en tiempo real.

Columnas obligatorias:

```txt
Hora
Comprar en
Precio Ask
Vender en
Precio Bid
Volumen disponible
Fees
Slippage
Ganancia neta estimada
Estado
Acción
```

Estados:

```txt
Rentable: success
Descartada: error
Ejecutada: info
Fallida: error
```

Acciones:

```txt
Ejecutar
Ver detalle
```

---

## 17. ExecutionPanel

Panel visual para explicar una simulación.

Debe mostrar:

```txt
Comprar BTC en Exchange A
Costos / transferencia simulada
Vender BTC en Exchange B
```

Bloques obligatorios:

```txt
Costo de compra
Ingreso por venta
Fees trading
Fee de retiro
Slippage
Penalización por latencia
Ganancia neta
Resultado final
```

La ganancia neta se muestra en verde si es positiva y rojo si es negativa.

---

## 18. WalletSummary

Debe mostrar balances simulados.

Columnas:

```txt
Exchange
BTC disponible
USDT disponible
Saldo bloqueado
Valor total USD
```

---

## 19. PerformanceCharts

Debe incluir:

```txt
P&L acumulado
Ganancia por par de exchanges
Oportunidades ejecutadas vs descartadas
Win rate
Tiempo promedio de ejecución
```

Colores de gráficos:

```txt
Ganancia: #03B987
Pérdida: #FA6C6E
Métrica neutral: #7EB0F3
```

---

## 20. SystemLogPanel

Panel tipo terminal.

Debe mostrar logs como:

```txt
14:32:18 [INFO] WebSocket Binance conectado
14:32:17 [SUCCESS] Simulación completada
14:31:58 [WARN] Oportunidad descartada por fees
14:30:45 [ERROR] Kraken feed reconectando
```

Colores:

```txt
INFO: #7EB0F3
SUCCESS: #03B987
WARN: #F4B740
ERROR: #FA6C6E
```

---

## 21. Pantallas obligatorias

Las pantallas se deben crear en este orden.

```txt
src/views/DashboardView.vue
src/views/OpportunitiesView.vue
src/views/OperationsView.vue
src/views/WalletsView.vue
src/views/PerformanceView.vue
src/views/LogsView.vue
src/views/SettingsView.vue
src/views/MarketsView.vue
```

---

## 22. Fases de implementación visual

### Fase 1 — Layout base

Componentes:

```txt
AppShell
AppSidebar
AppHeader
AppButton
AppCard
AppBadge
```

Objetivo:

```txt
Tener la estructura visual global lista.
```

---

### Fase 2 — Dashboard principal

Componentes:

```txt
KpiCard
ExchangeCard
OpportunityTable
ExecutionPanel
WalletSummary
PerformanceCharts
SystemLogPanel
```

Objetivo:

```txt
Tener la pantalla más importante lista para demo.
```

---

### Fase 3 — Oportunidades

Pantalla:

```txt
OpportunitiesView.vue
```

Debe incluir:

```txt
Resumen superior
Filtros
Tabla completa
Detalle lateral de oportunidad
```

---

### Fase 4 — Operaciones

Pantalla:

```txt
OperationsView.vue
```

Debe incluir:

```txt
KPIs
Tabla de operaciones
Detalle de operación
```

---

### Fase 5 — Wallets

Pantalla:

```txt
WalletsView.vue
```

Debe incluir:

```txt
Valor total simulado
Cards por exchange
Movimientos recientes
```

---

### Fase 6 — Rendimiento

Pantalla:

```txt
PerformanceView.vue
```

Debe incluir:

```txt
P&L acumulado
Ganancia por exchange pair
Win rate
Costos acumulados
Oportunidades por hora
```

---

### Fase 7 — Logs

Pantalla:

```txt
LogsView.vue
```

Debe incluir:

```txt
Filtros por nivel
Panel terminal
Estado de servicios
```

---

### Fase 8 — Configuración

Pantalla:

```txt
SettingsView.vue
```

Debe incluir:

```txt
Configuración de estrategia
Configuración de riesgo
Configuración de fees
Configuración de exchanges
Botones de guardar/restaurar
```

---

## 23. Dashboard principal: estructura visual establecida

```txt
DashboardView
├── KpiCard x6
├── ExchangeCard x3
├── OpportunityTable
├── ExecutionPanel
├── WalletSummary
├── PerformanceCharts
└── SystemLogPanel
```

Configuración del Grid:

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 16px;
}
```

Distribución para Desktop:

```txt
KPIs: 6 cards, cada una ocupa 2 columnas
Exchange cards: 3 cards, cada una ocupa 4 columnas
OpportunityTable: 7 columnas
ExecutionPanel: 5 columnas
WalletSummary: 4 columnas
PerformanceCharts: 5 columnas
Config summary: 3 columnas
SystemLogPanel: 12 columnas
```

---

## 24. Responsive

Prioridad principal: desktop.

### Desktop

```txt
Sidebar fija
Header fijo
Grid de 12 columnas
Tablas completas
```

### Tablet

```txt
Sidebar colapsable
Grid de 6 columnas
Tablas con scroll horizontal
```

### Mobile

```txt
Sidebar como drawer
Grid de 1 columna
Tablas con scroll horizontal
Cards apiladas
```

---

## 25. Estados obligatorios de UI

Cada pantalla debe contemplar:

```txt
Loading
Empty state
Error state
Disconnected state
Reconnecting state
```

Ejemplos:

```txt
No hay oportunidades detectadas todavía.
Esperando datos de WebSocket...
Kraken WebSocket desconectado. Reintentando conexión.
No se pudo cargar el historial de operaciones.
```

---

## 26. Reglas visuales para datos financieros

```txt
Ganancia positiva: verde #03B987
Pérdida: rojo #FA6C6E
Dato neutro: blanco
Texto secundario: #A8B0C3
Texto muy secundario: #6F7890
```

Ejemplos:

```txt
+$26.80 → verde
-$4.12 → rojo
0.02% → blanco
Actualizado hace 1s → gris
```

---

## 27. Reglas de nombres para componentes

Usar prefijos claros:

```txt
App     → componentes globales
Kpi     → métricas
Exchange → datos de exchange
Wallet  → saldos
Operation → operaciones simuladas
Opportunity → oportunidades de arbitraje
```

Ejemplos:

```txt
AppButton.vue
AppCard.vue
KpiCard.vue
ExchangeCard.vue
OpportunityTable.vue
OperationDetailPanel.vue
WalletMovementTable.vue
```

---

## 28. Arquitectura de directorios

```txt
src/
  assets/
  components/
    layout/
      AppShell.vue
      AppSidebar.vue
      AppHeader.vue

    ui/
      AppButton.vue
      AppCard.vue
      AppBadge.vue
      AppTable.vue
      AppInput.vue
      AppSelect.vue
      AppTabs.vue
      AppModal.vue
      AppEmptyState.vue
      AppLoadingState.vue
      AppErrorState.vue

    dashboard/
      KpiCard.vue
      ExchangeCard.vue
      OpportunityTable.vue
      ExecutionPanel.vue
      WalletSummary.vue
      PerformanceCharts.vue
      SystemLogPanel.vue

    markets/
      MarketTable.vue
      OrderBookDepth.vue
      ExchangeStatusCard.vue

    opportunities/
      OpportunityFilters.vue
      OpportunityDetailDrawer.vue

    operations/
      OperationHistoryTable.vue
      OperationDetailPanel.vue

    wallets/
      WalletCard.vue
      WalletMovementTable.vue

    settings/
      StrategySettingsForm.vue
      FeeSettingsTable.vue
      RiskSettingsForm.vue

  composables/
    useArbitrageSocket.ts
    useBotStatus.ts
    useMarketData.ts
    useOpportunities.ts

  router/
    index.ts

  stores/
    bot.store.ts
    market.store.ts
    opportunity.store.ts
    wallet.store.ts
    operation.store.ts

  styles/
    global.css
    variables.css

  views/
    DashboardView.vue
    MarketsView.vue
    OpportunitiesView.vue
    OperationsView.vue
    WalletsView.vue
    PerformanceView.vue
    LogsView.vue
    SettingsView.vue
```

---

## 29. Importación global de estilos

En `main.ts`:

```ts
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

import './styles/variables.css';
import './styles/global.css';

createApp(App)
  .use(createPinia())
  .use(router)
  .mount('#app');
```

---

## 30. Hoja de ruta (Roadmap) y Prioridades

Orden de implementación para el MVP:

```txt
1. Layout base
2. Dashboard principal
3. Oportunidades
4. Operaciones
5. Configuración
```

Pantallas secundarias:

```txt
Wallets
Rendimiento
Logs
Mercados
```

Pantalla crítica de lanzamiento:

```txt
Dashboard principal
```

Esta vista es el núcleo del sistema y debe integrar los componentes críticos.
