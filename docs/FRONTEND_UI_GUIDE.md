# FRONTEND_UI_GUIDE.md

# Guía oficial de interfaz frontend — ArbiBTC

Este documento define el sistema visual, componentes obligatorios y estructura frontend que se implementará en ArbiBTC. Todo el frontend debe seguir esta guía para mantener consistencia visual, mantenibilidad y velocidad de desarrollo.

---

## 1. Stack frontend oficial

- Vue 3.
- TypeScript.
- Vite.
- Pinia.
- Vue Router.
- Axios.
- WebSocket nativo encapsulado en composables.
- CSS global con variables.

---

## 2. Paleta oficial

```css
:root {
  --color-bg-dashboard: #0C0E1F;
  --color-bg-sidebar: #14172A;
  --color-primary-light: #7EB0F3;
  --color-primary-strong: #4451BB;
  --color-success: #03B987;
  --color-danger: #FA6C6E;
  --color-warning: #F4B740;
  --color-bg-card: #111529;
  --color-bg-card-soft: #171B33;
  --color-bg-terminal: #070A16;
  --color-border: rgba(255, 255, 255, 0.08);
  --color-text-primary: #FFFFFF;
  --color-text-secondary: #A8B0C3;
  --color-text-muted: #6F7890;

  --gradient-primary: linear-gradient(180deg, #7EB0F3 0%, #4451BB 100%);
}
```

---

## 3. Tipografía oficial

La fuente principal será:

```txt
Inter
```

Fallback:

```css
font-family: Inter, Manrope, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

Para números financieros se usará:

```txt
JetBrains Mono
```

Fallback:

```css
font-family: "JetBrains Mono", "IBM Plex Mono", Consolas, monospace;
```

---

## 4. Global style oficial

Archivo:

```txt
src/styles/globals.css
```

Contenido base:

```css
* {
  box-sizing: border-box;
}

html,
body,
#app {
  margin: 0;
  min-height: 100%;
  background: var(--color-bg-dashboard);
  color: var(--color-text-primary);
  font-family: Inter, Manrope, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

body {
  overflow: hidden;
}

button,
input,
select,
textarea {
  font: inherit;
}

a {
  color: inherit;
  text-decoration: none;
}

.numeric {
  font-family: "JetBrains Mono", "IBM Plex Mono", Consolas, monospace;
}

.text-success {
  color: var(--color-success);
}

.text-danger {
  color: var(--color-danger);
}

.text-muted {
  color: var(--color-text-muted);
}
```

---

## 5. Layout global

Todas las pantallas se renderizan dentro de `AppShell.vue`.

```txt
AppShell
├── AppSidebar
├── MainArea
│   ├── AppHeader
│   └── RouterView
```

### AppShell

Responsabilidad:

- Definir layout de dos columnas.
- Mantener sidebar fija.
- Mantener header fijo dentro del área principal.
- Renderizar la pantalla activa.

### AppSidebar

Color:

```txt
#14172A
```

Opciones:

- Dashboard.
- Mercados.
- Oportunidades.
- Operaciones.
- Wallets.
- Rendimiento.
- Logs.
- Configuración.

La opción activa usa:

```css
background: linear-gradient(180deg, #7EB0F3 0%, #4451BB 100%);
```

### AppHeader

Debe mostrar:

- Título de la pantalla.
- Subtítulo.
- Estado backend.
- Estado WebSockets.
- Estado motor del bot.
- Estado base de datos.
- Latencia.
- Botones `Iniciar Bot` y `Pausar`.

---

## 6. Componentes UI obligatorios

Estos componentes se implementan antes de cualquier pantalla compleja.

```txt
src/components/ui/
├── AppButton.vue
├── AppCard.vue
├── AppBadge.vue
├── AppTable.vue
├── AppInput.vue
├── AppSelect.vue
├── AppModal.vue
├── AppDrawer.vue
├── AppMetric.vue
└── AppEmptyState.vue
```

### AppButton

Variantes obligatorias:

- `primary`.
- `secondary`.
- `danger`.
- `ghost`.

`primary` usa el gradiente oficial.

### AppCard

Base visual:

```css
background: #111529;
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 16px;
padding: 20px;
```

### AppBadge

Estados:

- `success`.
- `danger`.
- `warning`.
- `info`.
- `neutral`.

### AppTable

Debe soportar:

- Headers.
- Rows.
- Loading.
- Empty state.
- Acciones por fila.
- Colores para profit/loss.

---

## 7. Componentes por dominio

### Dashboard

```txt
src/components/dashboard/
├── KpiCard.vue
├── ExchangeCard.vue
├── OpportunityTable.vue
├── ExecutionPanel.vue
├── WalletSummary.vue
├── PerformanceCharts.vue
└── SystemLogPanel.vue
```

### Oportunidades

```txt
src/components/opportunities/
├── OpportunityFilters.vue
├── OpportunityDetailDrawer.vue
└── OpportunityStatusBadge.vue
```

### Operaciones

```txt
src/components/operations/
├── OperationHistoryTable.vue
└── OperationDetailPanel.vue
```

### Wallets

```txt
src/components/wallets/
├── WalletCard.vue
└── WalletMovementTable.vue
```

### Logs

```txt
src/components/logs/
├── LogFilters.vue
└── TerminalLogPanel.vue
```

### Configuración

```txt
src/components/settings/
├── StrategySettingsForm.vue
├── RiskSettingsForm.vue
└── FeeSettingsTable.vue
```

---

## 8. Composables obligatorios

Los composables son parte oficial de la arquitectura frontend. No se coloca lógica de WebSocket, polling, formato ni suscripciones directamente dentro de componentes visuales.

```txt
src/composables/
├── useApi.ts
├── useDashboardSocket.ts
├── useBotStatus.ts
├── useMarketData.ts
├── useOpportunities.ts
├── useTrades.ts
├── useWallets.ts
├── useSystemLogs.ts
├── useFormatters.ts
└── useInterval.ts
```

### useDashboardSocket.ts

Responsabilidad:

- Abrir conexión WebSocket.
- Reintentar conexión.
- Escuchar eventos del backend.
- Redirigir eventos a stores de Pinia.
- Exponer estado `connected`, `latencyMs`, `lastMessageAt`.

### useFormatters.ts

Responsabilidad:

- Formatear USD.
- Formatear BTC.
- Formatear porcentajes.
- Formatear fechas.
- Formatear estados.

---

## 9. Stores oficiales

```txt
src/stores/
├── dashboard.store.ts
├── market.store.ts
├── opportunities.store.ts
├── trades.store.ts
├── wallets.store.ts
├── logs.store.ts
├── bot.store.ts
└── settings.store.ts
```

Los stores mantienen el estado. Los componentes solo renderizan y emiten acciones.

---

## 10. Services oficiales

```txt
src/services/
├── http.ts
├── dashboard.service.ts
├── market.service.ts
├── opportunities.service.ts
├── trades.service.ts
├── wallets.service.ts
├── logs.service.ts
└── settings.service.ts
```

`http.ts` configura Axios con `VITE_API_BASE_URL`.

---

## 11. Views oficiales

```txt
src/views/
├── DashboardView.vue
├── MarketsView.vue
├── OpportunitiesView.vue
├── OperationsView.vue
├── WalletsView.vue
├── PerformanceView.vue
├── LogsView.vue
└── SettingsView.vue
```

---

## 12. Pantalla Dashboard

El dashboard incluye:

1. KPI cards.
2. Exchange cards.
3. Tabla de oportunidades en tiempo real.
4. Panel de ejecución simulada.
5. Wallet summary.
6. Gráficos de rendimiento.
7. Logs del sistema.

Esta pantalla se construye primero.

---

## 13. Orden de implementación frontend

1. Variables CSS y global style.
2. Layout base.
3. Componentes UI.
4. Router.
5. Services REST.
6. Stores Pinia.
7. Composables.
8. Dashboard con datos REST.
9. WebSocket dashboard.
10. Pantallas secundarias.
11. Loading, empty y error states.
12. Ajustes responsive.

---

## 14. Criterio de aceptación frontend

### Paleta de Colores Oficial (Navy Dark)
*   **Fondo Base:** `#0B0E14`
*   **Fondo Sidebar:** `#0F121E`
*   **Fondo Tarjetas:** `#151826` y `#1A1D2D`
*   **Acento Primario:** `#3B82F6` a `#2563EB` (gradiente)
*   **Éxito:** `#10B981` (Minimalista vibrante)
*   **Peligro:** `#EF4444`
*   **Texto Principal:** `#E2E8F0`
*   **Texto Muted:** `#64748B`

### Tipografía
*   **Fuente Principal:** `Inter` (sans-serif) para la interfaz general.
*   **Fuente Numérica/Logs:** `JetBrains Mono` (monospace) para montos, precios y consola.
*   **Estilo Dashboard:** Uso extensivo de `.uppercase-label` (font-size: 11px, letter-spacing: 0.08em) para etiquetas secundarias.

### Iconografía
*   **Librería:** Google Material Symbols (Outlined) cargado vía CDN para consistencia estética y peso ligero.

El frontend se considera correcto cuando:

- Respeta la paleta oficial.
- Usa layout global.
- No mezcla lógica de red dentro de componentes visuales.
- Usa composables para WebSockets y lógica reusable.
- Usa stores para estado global.
- El dashboard recibe eventos en tiempo real.
- Las pantallas principales consumen el contrato API oficial.
